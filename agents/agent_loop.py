import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'task_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'analytics_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'reward_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'memory'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from openai import OpenAI
import agent_tools
from task_tools import list_tasks, assign_task, get_user_capacity
from analytics_tools import get_engagement_metrics
from reward_tools import suggest_reward, update_points_ledger
from memory_manager import load_shared_memory, save_shared_memory

client = OpenAI(base_url="http://localhost:10000/v1", api_key="ollama")

def run_tool(name, inp):
    try:
        if name == "list_tasks":
            return list_tasks(inp.get("taskStatus"))
        if name == "assign_task":
            return assign_task(inp["task_id"], inp["user_id"], inp["due_date"], inp.get("reason"))
        if name == "get_user_capacity":
            return get_user_capacity(inp["user_id"])
        if name == "get_engagement_metrics":
            return get_engagement_metrics(inp["user_id"])
        if name == "suggest_reward":
            return suggest_reward(inp["user_id"])
        if name == "update_points_ledger":
            return update_points_ledger(inp["user_id"], inp["task_id"], inp["status"])
    except KeyError as e:
        return f"Error: missing required parameter {e}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_agent(agent_name, agent_type, messages):
    if agent_type == "orchestrator":
        tools = [agent_tools.list_task, agent_tools.assign_task, agent_tools.get_user_capacity, agent_tools.get_engagement_metrics]
    else:
        tools = [agent_tools.get_engagement_metrics, agent_tools.suggest_reward, agent_tools.update_points_ledger]

    max_iters = 10
    iters = 0

    response = client.chat.completions.create(
        model="granite4:latest",
        max_tokens=2000,
        tools=tools,
        messages=messages
    )

    while response.choices[0].finish_reason == "tool_calls" and iters < max_iters:
        iters += 1
        msg = response.choices[0].message
        
        msg_dict = {"role": "assistant", "content": msg.content}
        if msg.tool_calls:
            msg_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in msg.tool_calls
            ]
        messages.append(msg_dict)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  -> {agent_name} calling {name}")
            result = run_tool(name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        response = client.chat.completions.create(
            model="granite4:latest",
            max_tokens=2000,
            tools=tools,
            messages=messages
        )

    reply = response.choices[0].message.content
    if reply:
        print(f"\n[{agent_name}] {reply}")
        messages.append({"role": "assistant", "content": reply})
    return messages

def main():
    print("=" * 60)
    print("ChoreQuest Multi-Agent System")
    print("=" * 60)

    memory = load_shared_memory()
    orchestrator_messages = memory.get("orchestrator_messages", [])
    motivator_messages = memory.get("motivator_messages", [])

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("\nWhat should the agents do? ").strip()

    if not user_input:
        user_input = "Assign all pending tasks to family members and analyze engagement"

    print(f"\nInput: {user_input}\n")

    print("Phase 1: Orchestrator (Task Assignment)")
    print("-" * 60)

    if not orchestrator_messages:
        orchestrator_messages = [
            {"role": "system", "content": "You are the Task Orchestrator Agent. Do these steps in order: 1) Call list_tasks(taskStatus='pending') 2) Call get_user_capacity(user_id='emma'), get_user_capacity(user_id='john'), get_user_capacity(user_id='lily') 3) Assign 3 tasks: assign_task(task_id='task_1', user_id='emma', due_date='2026-07-10'), assign_task(task_id='task_6', user_id='lily', due_date='2026-07-10'), assign_task(task_id='task_3', user_id='john', due_date='2026-07-10'). Call all tools in this exact order."}
        ]

    orchestrator_messages.append({"role": "user", "content": user_input})
    orchestrator_messages = run_agent("Orchestrator", "orchestrator", orchestrator_messages)

    print("\n\nPhase 2: Motivator (Engagement Analysis)")
    print("-" * 60)

    if not motivator_messages:
        motivator_messages = [
            {"role": "system", "content": "You are the Motivator Agent. You MUST call tools to get real data. First call get_engagement_metrics() for each child (emma, john, lily). Then call suggest_reward() for top performers. Never guess user IDs - always use the tool results."}
        ]

    context = "The Orchestrator just finished assigning tasks. Now analyze engagement for each family member - check metrics, suggest rewards for top performers, flag anyone at risk."
    motivator_messages.append({"role": "user", "content": context})
    motivator_messages = run_agent("Motivator", "motivator", motivator_messages)

    memory["orchestrator_messages"] = orchestrator_messages
    memory["motivator_messages"] = motivator_messages
    save_shared_memory(memory)

    print("\n" + "=" * 60)
    print("Done. Memory saved to shared_memory.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
