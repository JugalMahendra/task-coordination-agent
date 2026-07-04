# Task Coordination Agent — Project State

**Date:** July 4, 2026
**Course:** Kaggle AI Agents Capstone (Deadline: July 6, 2026)

---

## Files Built

### 1. `seed_data.py` — Data layer
- **FAMILY:** 5 members (mom, dad, emma, john, lily) with id, name, role, age
- **TASKS:** 6 chores (Wash dishes, Take out trash, Vacuum, Clean bathroom, Mow lawn, Set table) with difficulty, points, status
- **TASKS_ASSIGNMENT:** Assignment history (who did what, when, status)
- **Helpers:** `get_task()`, `get_user()`, `get_completions_for_user()`, `get_points_balance()`, etc.

### 2. `mcp_server.py` — MCP tool implementations
- **list_tasks(status)** — Returns tasks filtered by status (or all)
- **assign_task(task_id, user_id, due_date, reason)** — Validates + appends to TASKS_ASSIGNMENT
- **get_user_capacity(user_id)** — Counts assigned tasks for a user
- **get_engagement_metrics(user_id)** — Returns completion rate, points, task load
- **suggest_reward(user_id)** — Suggests affordable reward based on points
- **update_points_ledger(user_id, task_id, status)** — Updates task assignment status

### 3. `agent_tools.py` — Tool definitions (OpenAI-compatible format)
Defines all 6 tools as `{"type": "function", "function": {"name": ..., "parameters": ...}}` for the LLM API.

### 4. `agent_loop.py` — Main agent loop
- Loads memory from `memory.json` (conversation + assignments persist between sessions)
- Connects to local LLM via OpenAI-compatible API (Msty at port 10000)
- Tool calling loop: handles tool_use, dispatches to mcp_server, returns results
- Saves memory after each message
- Interactive chat interface

### 5. `motivator_agent.py` — Agent 2 (Motivator)
- Tracks engagement, suggests rewards, flags at-risk members
- Uses same agent loop pattern as agent_loop.py
- 3 tools: get_engagement_metrics, suggest_reward, update_points_ledger

### 6. `multi_agent_orchestrator.py` — Two-phase multi-agent system
- Phase 1: Orchestrator assigns tasks (list_tasks, assign_task, get_user_capacity)
- Phase 2: Motivator analyzes engagement (get_engagement_metrics, suggest_reward)
- Uses qwen3:latest model
- Results saved to shared_memory.json

### 7. `main_agent.py` — Combined single-loop agent
- All 6 tools in one agent loop
- Alternative to multi_agent_orchestrator.py

---

## Architecture

```
You → multi_agent_orchestrator.py → LLM (qwen3:latest via Msty)
                                          ↓
                               Phase 1: Orchestrator (3 tools)
                                          ↓
                               Phase 2: Motivator (3 tools)
                                          ↓
                               shared_memory.json → result → you
```

## How to Run

```bash
# Multi-agent system (recommended)
py multi_agent_orchestrator.py "assign all pending tasks"

# Single agent (alternative)
py main_agent.py

# Interactive chat
py agent_loop.py
```

## Current Model: granite4:latest (via Msty at localhost:10000)

## Memory System
- `memory.json` stores conversation history + assignments
- `shared_memory.json` stores multi-agent results (Orchestrator output → Motivator input)
- Both files enable continuing conversations across sessions

## What Was Built — Step by Step (from ARCHITECTURE.md)

| Step | What | Status |
|------|------|--------|
| 1 | Project setup | ✅ |
| 2 | Fake data (seed_data.py) | ✅ |
| 3 | MCP server (mcp_server.py) | ✅ 6 tools |
| 4 | Agent 1: Orchestrator | ✅ |
| 5 | Agent 2: Motivator | ✅ |
| 6 | Wire agents together | ✅ (multi_agent_orchestrator.py) |
| 7 | Test and iterate | ✅ Working! |
| 8 | Demo video | ⬜ |

## Known Issues
- None currently - granite4:latest works with tool calling

## Next Steps
1. Record demo video
