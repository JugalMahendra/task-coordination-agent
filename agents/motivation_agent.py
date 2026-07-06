import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'analytics_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'reward_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from openai import OpenAI
import agent_tools
from analytics_tools import get_engagement_metrics
from reward_tools import suggest_reward, update_points_ledger

client = OpenAI(base_url="http://localhost:10000/v1", api_key="ollama")

def run_tool(name, inp):
    try:
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

def run_motivation(user_input, messages=None):
    tools = [agent_tools.get_engagement_metrics, agent_tools.suggest_reward, agent_tools.update_points_ledger]

    if messages is None:
        messages = [
            {"role": "system", "content": "You are the Motivator Agent. After tasks are assigned, analyze engagement for each family member. Check completion rates, suggest rewards, flag at-risk members. Always call tools to get real data."}
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
            print(f"  -> Motivator calling {name}")
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
        print(f"\n[Motivator] {reply}")
        messages.append({"role": "assistant", "content": reply})
    return messages
