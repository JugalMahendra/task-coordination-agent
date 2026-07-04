import json
import sys
from datetime import datetime
import agent_tools
from openai import OpenAI
from mcp_server import list_tasks, assign_task, get_user_capacity

MEMORY_FILE = "memory.json"
session_log = []

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"messages": [], "assignments": []}

def save_memory():
    state = {
        "messages": messages,
        "assignments": get_assignments(),
        "saved_at": str(datetime.now())
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

def get_assignments():
    from seed_data import TASKS_ASSIGNMENT
    return TASKS_ASSIGNMENT

def run_tool(name, inp):
    try:
        if name == "list_tasks":
            return list_tasks(inp.get("taskStatus"))
        if name == "assign_task":
            return assign_task(inp["task_id"], inp["user_id"], inp["due_date"], inp.get("reason"))
        if name == "get_user_capacity":
            return get_user_capacity(inp["user_id"])
    except KeyError as e:
        return f"Error: missing required parameter {e} for tool {name}. Check the tool definition and provide all required fields."

tools = [agent_tools.list_task, agent_tools.assign_task, agent_tools.get_user_capacity]
client = OpenAI(base_url="http://localhost:10000/v1", api_key="ollama")

memory = load_memory()

from seed_data import TASKS_ASSIGNMENT
TASKS_ASSIGNMENT.clear()
TASKS_ASSIGNMENT.extend(memory["assignments"])

messages = memory["messages"] if memory["messages"] else [
    {"role": "system", "content": "You are the Task Orchestrator Agent. Your job is to assign pending tasks to family members. Rules: - No one gets more than 3 tasks per day - Match difficulty to age (easy to younger kids) - Consider preferences from history. Always call the available functions to get real data before answering. Never describe what you would do — just do it."}
]

print(f"Task Coordination Agent chat started. Type 'quit' to exit.\nLoaded {len(memory['messages'])} previous messages, {len(memory['assignments'])} past assignments.\n")

# If we receive command line arguments, use them as user input
if len(sys.argv) > 1:
    user_inputs = sys.argv[1:]
    for user_input in user_inputs:
        messages.append({"role": "user", "content": user_input})
        session_log.append({"role": "user", "content": user_input})

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
                result = run_tool(name, args)
                session_log.append({"tool": name, "args": args, "result": str(result)})
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
            print(f"\nAgent: {reply}")
            messages.append({"role": "assistant", "content": reply})
            session_log.append({"role": "assistant", "content": reply})
        save_memory()
else:
    # Interactive mode
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user_input})
        session_log.append({"role": "user", "content": user_input})

    messages.append({"role": "user", "content": user_input})
    session_log.append({"role": "user", "content": user_input})

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
            result = run_tool(name, args)
            session_log.append({"tool": name, "args": args, "result": str(result)})
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
        print(f"\nAgent: {reply}")
        messages.append({"role": "assistant", "content": reply})
        session_log.append({"role": "assistant", "content": reply})
    save_memory()

save_memory()
print(f"Memory saved to {MEMORY_FILE} ({len(TASKS_ASSIGNMENT)} assignments stored)")
print("Goodbye!")
