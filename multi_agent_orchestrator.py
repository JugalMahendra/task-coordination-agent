import json
import sys
from datetime import datetime
import agent_tools
from openai import OpenAI
from mcp_server import (list_tasks, assign_task, get_user_capacity,
                        get_engagement_metrics, suggest_reward, update_points_ledger)

SHARED_MEMORY_FILE = "shared_memory.json"

def load_shared_memory():
    try:
        with open(SHARED_MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "orchestrator_messages": [],
            "motivator_messages": [],
            "assignments": [],
            "created_at": str(datetime.now())
        }

def save_shared_memory(state):
    with open(SHARED_MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

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

client = OpenAI(base_url="http://localhost:10000/v1", api_key="ollama")

ORCHESTRATOR_TOOLS = [agent_tools.list_task, agent_tools.assign_task, agent_tools.get_user_capacity, agent_tools.get_engagement_metrics]
MOTIVATOR_TOOLS = [agent_tools.get_engagement_metrics, agent_tools.suggest_reward, agent_tools.update_points_ledger]

def run_agent(agent_name, agent_type, messages):
    tools = ORCHESTRATOR_TOOLS if agent_type == "orchestrator" else MOTIVATOR_TOOLS

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
        messages.append(msg)

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

# Phase 1: Orchestrator
print("Phase 1: Orchestrator (Task Assignment)")
print("-" * 60)

if not orchestrator_messages:
    orchestrator_messages = [
        {"role": "system", "content": "You are the Task Orchestrator Agent. Assign pending tasks to family members. Rules: max 3 tasks per person, match difficulty to age, check capacity. Always call tools to get real data."}
    ]

orchestrator_messages.append({"role": "user", "content": user_input})
orchestrator_messages = run_agent("Orchestrator", "orchestrator", orchestrator_messages)

# Phase 2: Motivator
print("\n\nPhase 2: Motivator (Engagement Analysis)")
print("-" * 60)

if not motivator_messages:
    motivator_messages = [
        {"role": "system", "content": "You are the Motivator Agent. After tasks are assigned, analyze engagement for each family member. Check completion rates, suggest rewards, flag at-risk members. Always call tools to get real data."}
    ]

context = "The Orchestrator just finished assigning tasks. Now analyze engagement for each family member - check metrics, suggest rewards for top performers, flag anyone at risk."
motivator_messages.append({"role": "user", "content": context})
motivator_messages = run_agent("Motivator", "motivator", motivator_messages)

# Save
memory["orchestrator_messages"] = orchestrator_messages
memory["motivator_messages"] = motivator_messages
memory["updated_at"] = str(datetime.now())
save_shared_memory(memory)

print("\n" + "=" * 60)
print("Done. Memory saved to shared_memory.json")
print("=" * 60)
