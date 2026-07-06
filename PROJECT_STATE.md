# Task Coordination Agent — Project State

**Date:** July 5, 2026
**Course:** Kaggle AI Agents Capstone (Deadline: July 6, 2026)

---

## Project Structure

```
task-coordination-agent/
│
├── agents/
│   ├── orchestrator.py          # Central decision-making and coordination logic
│   ├── engagement_agent.py      # Tracks participation and workload patterns
│   ├── motivation_agent.py      # Generates rewards and motivation signals
│   ├── communication_agent.py   # Handles notifications and messaging
│   └── agent_loop.py            # Main execution cycle (runtime loop)
│
├── mcp_servers/
│   ├── task_tools/              # Task management (create, assign, update)
│   │   └── task_tools.py
│   ├── analytics_tools/         # Engagement + workload analytics
│   │   └── analytics_tools.py
│   ├── reward_tools/            # Incentive and motivation logic
│   │   └── reward_tools.py
│   └── communication_tools/     # Messaging and notification tools
│       └── communication_tools.py
│
├── memory/
│   ├── shared_memory.json       # Persistent system state across cycles
│   └── memory_manager.py        # Read/write abstraction layer for memory
│
├── scripts/
│   ├── seed_demo.py             # Demo data + example execution flow
│   └── run_system.bat           # System startup script
│
├── docs/
│   ├── ARCHITECTURE.md          # System design overview
│   ├── KAGGLE_WRITEUP.md        # Kaggle submission writeup
│   └── NEXT_STEPS.md            # Timeline and next actions
│
├── benchmark/
│   ├── scenarios.json           # 10 test scenarios
│   ├── run_benchmark.py         # Benchmark runner
│   └── README.md                # Benchmark documentation
│
├── agent_tools.py               # Tool definitions (OpenAI format)
├── seed_data.py                 # Original data layer
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```

## How to Run

```bash
# Make sure Msty is running with granite4 loaded
py agents/agent_loop.py "assign all pending tasks"

# Or use the batch script
scripts\run_system.bat "check tasks"
```

## Current Model: granite4:latest (via Msty at localhost:10000)

## Files Built

### Agents
- **orchestrator.py** — Task assignment with reasoning
- **engagement_agent.py** — Tracks participation, detects at-risk members
- **motivation_agent.py** — Analyzes engagement, suggests rewards
- **communication_agent.py** — Notifications and reminders
- **agent_loop.py** — Main runtime loop (Orchestrator → Motivator)

### MCP Servers
- **task_tools.py** — list_tasks, assign_task, get_user_capacity
- **analytics_tools.py** — get_engagement_metrics
- **reward_tools.py** — suggest_reward, update_points_ledger
- **communication_tools.py** — send_notification, send_reminder, send_encouragement

### Memory
- **memory_manager.py** — Read/write abstraction for shared_memory.json

## Course Concepts Demonstrated

| Concept | Status |
|---------|--------|
| Multi-Agent Systems (ADK) | ✅ |
| MCP Servers | ✅ 6 tools |
| Tool Use | ✅ |
| Security | ✅ Local LLM |
| Deployability | ✅ Offline |

## Next Steps
1. Record demo video
2. Upload to YouTube
3. Submit to Kaggle
