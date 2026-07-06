import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'task_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'analytics_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from openai import OpenAI
import agent_tools
from task_tools import list_tasks, assign_task, get_user_capacity
from analytics_tools import get_engagement_metrics

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
    except KeyError as e:
        return f"Error: missing required parameter {e}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_orchestrator(user_input, messages=None):
    tools = [agent_tools.list_task, agent_tools.assign_task, agent_tools.get_user_capacity, agent_tools.get_engagement_metrics]

    if messages is None:
        messages = [
            {"role": "system", "content": "You are the Task Orchestrator Agent. Assign pending tasks to family members. Rules: max 3 tasks per person, match difficulty to age, check capacity. Always call tools to get real data."}
        ]

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="granite4:latest",
        max_tokens=2000,
        tools=tools,
        messages=messages
    )

    max_iters = 10
    iters = 0

    while response.choices[0].finish_reason == "tool_calls" and iters < max_iters:
        iters += 1
        msg = response.choices[0].message
        messages.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  -> Orchestrator calling {name}")
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
        print(f"\n[Orchestrator] {reply}")
        messages.append({"role": "assistant", "content": reply})
    return messages
