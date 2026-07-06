import json
import time
from openai import OpenAI
import agent_tools
from mcp_server import (list_tasks, assign_task, get_user_capacity,
                        get_engagement_metrics, suggest_reward, update_points_ledger)

SCENARIOS_FILE = "benchmark/scenarios.json"
RESULTS_FILE = "benchmark/results.json"

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
    except Exception as e:
        return f"Error: {str(e)}"

def test_scenario(scenario):
    tools = [agent_tools.list_task, agent_tools.assign_task, agent_tools.get_user_capacity,
             agent_tools.get_engagement_metrics, agent_tools.suggest_reward, agent_tools.update_points_ledger]

    messages = [
        {"role": "system", "content": "You are a task coordination agent. Use tools to help manage family chores."},
        {"role": "user", "content": scenario["query"]}
    ]

    start_time = time.time()
    tool_calls_made = []

    try:
        response = client.chat.completions.create(
            model="granite4:latest",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        while response.choices[0].finish_reason == "tool_calls":
            msg = response.choices[0].message
            messages.append(msg)

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                tool_calls_made.append({"name": name, "args": args})
                result = run_tool(name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            response = client.chat.completions.create(
                model="granite4:latest",
                max_tokens=1000,
                tools=tools,
                messages=messages
            )

        elapsed = time.time() - start_time
        return {
            "success": True,
            "tool_calls": tool_calls_made,
            "time_seconds": round(elapsed, 2),
            "final_response": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tool_calls": tool_calls_made,
            "time_seconds": round(time.time() - start_time, 2)
        }

def evaluate_results(scenario, result):
    if not result["success"]:
        return {"passed": False, "reason": "execution_failed"}

    expected_tools = set(scenario["expected_tools"])
    actual_tools = set(tc["name"] for tc in result["tool_calls"])

    tool_selection_correct = expected_tools.issubset(actual_tools)
    tools_called = len(result["tool_calls"]) > 0

    return {
        "passed": tool_selection_correct and tools_called,
        "tool_selection_correct": tool_selection_correct,
        "expected_tools": list(expected_tools),
        "actual_tools": list(actual_tools),
        "tools_called_count": len(result["tool_calls"])
    }

def main():
    with open(SCENARIOS_FILE, "r") as f:
        benchmark = json.load(f)

    results = {
        "benchmark_name": benchmark["benchmark_name"],
        "model": "granite4:latest",
        "scenarios": [],
        "summary": {}
    }

    total = len(benchmark["scenarios"])
    passed = 0

    print("=" * 60)
    print("ChoreQuest Benchmark Runner")
    print("=" * 60)

    for scenario in benchmark["scenarios"]:
        print(f"\nTesting: {scenario['id']} - {scenario['query'][:50]}...")

        result = test_scenario(scenario)
        evaluation = evaluate_results(scenario, result)

        scenario_result = {
            "id": scenario["id"],
            "query": scenario["query"],
            "difficulty": scenario["difficulty"],
            "result": result,
            "evaluation": evaluation
        }
        results["scenarios"].append(scenario_result)

        status = "PASS" if evaluation["passed"] else "FAIL"
        print(f"  [{status}] Tools called: {len(result['tool_calls'])}, Time: {result['time_seconds']}s")

        if evaluation["passed"]:
            passed += 1

    results["summary"] = {
        "total_scenarios": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round((passed / total) * 100, 1)
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} passed ({results['summary']['pass_rate']}%)")
    print(f"Saved to: {RESULTS_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
