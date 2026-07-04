# ChoreQuest: Intelligent Multi-Agent Task Coordination for Families

## Overview

Family chore management is a persistent challenge that impacts household dynamics, parental stress, and children's development. ChoreQuest is an AI-powered multi-agent system that intelligently coordinates task assignments, tracks family engagement, and maintains motivation through adaptive incentive mechanisms. By leveraging granite4's reasoning capabilities and a specialized two-agent architecture, ChoreQuest transforms ad-hoc chore management into a fair, transparent, and psychologically informed system.

---

## Problem Statement

### The Challenge

Managing household chores across multiple family members presents three interconnected challenges:

**1. Unfair Task Distribution**
Parents assign chores based on availability or convenience rather than capacity, ability, or fairness. Emma might accumulate difficult tasks while John gets easy ones, creating resentment and disengagement.

**2. Invisible Workload**
Parents lack clear visibility into who is overloaded. A child might have 5 incomplete tasks but parents don't realize, leading to frustration on both sides. There's no systematic way to understand individual capacity.

**3. Generic Motivation Fails**
Standard reward systems (points, badges) don't adapt to what actually motivates each child. Emma might value screen time while John wants outdoor activities. Generic incentives create disengagement.

### Why AI Agents Matter

Traditional solutions fail because they're either:
- **Too rigid** (fixed chore schedules ignore preferences)
- **Too manual** (parents manually track everything)
- **Not intelligent** (no reasoning about fairness or burnout)

AI agents uniquely address this through:
- **Reasoning**: Agents analyze capacity, preferences, and fairness together
- **Tool integration**: Agents call functions to access real data, not guess
- **Adaptation**: Agents learn what works for each person
- **Collaboration**: Multiple agents with different expertise work together

---

## Solution Design

### Architecture Overview

ChoreQuest uses a **two-agent system** where each agent has specialized expertise:

**Agent 1: Task Orchestrator**
- *Role:* Intelligent task assignment
- *Responsibility:* Ensure fair distribution matching capacity and preferences
- *Key capability:* Reasoning about tradeoffs (fairness vs. preference vs. difficulty)

**Agent 2: Engagement & Motivator**
- *Role:* Maintain engagement and motivation
- *Responsibility:* Detect at-risk members, celebrate wins, personalize incentives
- *Key capability:* Trend analysis and intervention recommendations

### How Agents Collaborate

```
User Input: "Assign pending chores"
    ↓
[Orchestrator Agent]
  → Calls: list_tasks(), get_user_capacity(), get_engagement_metrics()
  → Analyzes: capacity limits, preferences, fairness
  → Executes: assign_task() for each person
  → Output: Fair assignments with reasoning
    ↓
[Shared Context: JSON Memory + Orchestrator Results]
    ↓
[Motivator Agent]
  → Reads: Orchestrator's assignments
  → Calls: get_engagement_metrics() for each person
  → Analyzes: Will assignments improve/harm engagement?
  → Executes: update_points_ledger() for bonuses
  → Output: Motivation strategies + recognition
    ↓
Both agents save to shared_memory.json
```

### Why This Design

1. **Separation of Concerns**: Each agent focuses on its expertise (assignment vs. motivation)
2. **Intelligent Collaboration**: Orchestrator doesn't need to know about motivation; Motivator builds on Orchestrator's work
3. **Extensibility**: Easy to add more agents (e.g., Communication agent for reminders, Analytics agent for insights)
4. **Transparency**: Each agent explains its reasoning to users

---

## Technical Implementation

### Core Technologies

- **LLM**: granite4 (local, fast, efficient)
- **Framework**: OpenAI-compatible API via Msty (localhost:10000)
- **Data Storage**: JSON-based persistent memory
- **Language**: Python 3.x

### The 6 MCP Tools

All tools are fully implemented with validation and error handling:

#### 1. `list_tasks(taskStatus)`
```python
# Gets pending/assigned/completed chores
# Example output:
[
    {"task_id": "task_1", "title": "Wash dishes", "difficulty": "medium", 
     "points": 20, "status": "pending"},
    ...
]
```

**What agents use it for:**
- Orchestrator: See what needs assigning
- Motivator: Understand current workload context

#### 2. `assign_task(task_id, user_id, due_date, reason)`
```python
# Assigns a task to someone
# Example:
assign_task("task_1", "emma", "2026-06-27", 
            reason="Emma has 95% success with dishes, only 1 current task")
```

**What orchestrator does:** Makes actual assignments with reasoning

#### 3. `get_user_capacity(user_id)`
```python
# Returns current workload count
# Example output: 2 (number of assigned tasks)
```

**What orchestrator does:** Checks before assigning new tasks

#### 4. `get_engagement_metrics(user_id)`
```python
# Rich engagement data
{
  "user_id": "emma",
  "name": "Emma",
  "total_assigned": 20,
  "completed": 19,
  "failed": 1,
  "completion_rate": 95.0,
  "points_balance": 150,
  "current_capacity": 2
}
```

**What agents use it for:**
- Orchestrator: Understand preferences from history
- Motivator: Analyze engagement patterns

#### 5. `suggest_reward(user_id)`
```python
# Personalized reward suggestions
{
  "user_id": "emma",
  "name": "Emma",
  "points_balance": 150,
  "affordable_rewards": [
    {"name": "Choose dinner", "cost": 60},
    {"name": "Stay up 30 min late", "cost": 40}
  ],
  "suggestion": {"name": "Choose dinner", "cost": 60}
}
```

**What motivator does:** Suggests appropriate rewards

#### 6. `update_points_ledger(user_id, task_id, status)`
```python
# Update task status (completed, failed, in_progress)
# Example: Mark task as completed
update_points_ledger("emma", "task_1", "completed")
```

**What motivator does:** Updates status and tracks progress

### Agent Reasoning Loop

```python
# Simplified orchestrator reasoning
response = client.chat.completions.create(
    model="granite4:latest",
    messages=[
        {"role": "system", "content": "You are the Task Orchestrator..."},
        {"role": "user", "content": "Assign all pending chores"}
    ],
    tools=[list_tasks, assign_task, get_user_capacity, get_engagement_metrics]
)

# Qwen reasons about which tools to call
# If response.tool_use:
#   - Call list_tasks() → get pending items
#   - For each person: call get_user_capacity() → check capacity
#   - For each person: call get_engagement_metrics() → understand preferences
#   - For best matches: call assign_task() with reasoning
#
# Qwen then generates final response explaining assignments
```

### Persistent Memory System

```python
# Memory structure
{
  "orchestrator_messages": [...],    # Full conversation history
  "motivator_messages": [...],
  "assignments": [...],              # Past assignments for learning
  "updated_at": "2026-06-26T12:00:00"
}
```

**Benefits:**
- Agents remember previous preferences
- System learns over time ("Emma prefers evening tasks")
- Multi-session continuity ("I remember John had burnout last week")

---

## Implementation Highlights

### 1. Local LLM for Speed and Privacy

ChoreQuest runs granite4 locally via Msty, providing:
- **No API costs**: Runs on your machine
- **Privacy**: Family data never leaves your computer
- **Speed**: Fast inference with minimal GPU usage
- **Offline**: Works without internet connection

### 2. Intelligent Reasoning

The Orchestrator doesn't just assign tasks randomly. It reasons through tradeoffs:

**Example orchestrator prompt:**
```
"Emma (age 12) has completed 19 of 20 assigned tasks (95% success).
She prefers evening work and dislikes water-based chores. Currently has 
1 task assigned. John (age 10) has completed 12 of 20 (60% success), 
prefers outdoor tasks, currently has 2 assigned.

Given these two pending tasks - 'Wash dishes' and 'Rake yard' - 
where difficulty is medium/hard respectively, how should I assign them?"

Agent response: "Assign dishes to Emma (her strength, evening preference, 
has capacity) and yard to John (outdoor preference, lighter work since 
he's at 60% completion)."
```

### 3. Multi-Turn Tool Calling

Agents don't make assumptions; they query tools:

```
Turn 1: User says "Assign chores"
Turn 2: Orchestrator calls list_tasks()
        → "Found 3 pending: dishes, vacuum, trash"
Turn 3: Orchestrator calls get_user_capacity() for each person
        → "Emma: 2 slots, John: 1 slot, Lily: 3 slots"
Turn 4: Orchestrator calls get_engagement_metrics() for each
        → "Emma: 95%, John: 60%, Lily: new member"
Turn 5: Orchestrator calls assign_task() with reasoning
        → "Assigning dishes to Emma..."
```

This ensures decisions are data-driven, not hallucinated.

### 4. Motivator Agent's Intelligence

The Motivator doesn't just award points randomly. It understands:

**Trend Analysis**
```python
# If Emma's completion rate dropped from 95% → 85% last week
# Motivator detects declining trend
# Recommends: Check in with Emma, maybe tasks are too hard
```

**At-Risk Detection**
```python
# Signals that trigger intervention:
# - No activity 7+ days → disengagement
# - 5+ overdue tasks → burnout
# - Completion rate < 50% → struggling
```

**Personalized Recognition**
```python
# Generic: "Good job!"
# ChoreQuest: "You completed 5 chores this week with 95% success rate.
#              That's your best week ever! +10 bonus points"
```

### 5. Error Handling & Validation

Every tool validates inputs:

```python
def assign_task(task_id, user_id, due_date, reason=""):
    # Check task exists
    task = get_task(task_id)
    if task is None:
        return f"Task with {task_id} Not Found"
    
    # Check user exists
    if get_user(user_id) is None:
        return f"User with {user_id} Not Found"
    
    # Only if all checks pass: execute assignment
    ...
```

---

## Results & Impact

### What the System Can Do

**Real-Time Task Assignment**
```
Input: "Assign all pending chores"

Output from Orchestrator:
- Dishes → Emma (95% history, loves it, has capacity)
- Vacuum → John (outdoor preference, lighter load)
- Trash → Lily (confidence-building task)

Output from Motivator:
- Emma: Excellent performer (95% completion)
- John: At-risk (60% completion, needs support)
- Lily: New member (build confidence with easy tasks)
```

**Engagement Analysis**
```
Input: "Analyze family engagement"

Output:
- Emma: Excellent (95% completion, stable)
  Recommendation: Stretch challenges, maintain streak
  
- John: Moderate (60%, declining)
  Alert: Overload detected (5 pending tasks)
  Recommendation: Reduce workload, offer support
  
- Lily: New member
  Recommendation: Build confidence with easy tasks
```

**Risk Detection**
```
Input: "Check on John"

Output:
At-Risk Alert: John shows burnout signals
- Assigned 5 tasks, completed 2
- No activity 3 days
- Completion rate declining from 75% → 60%

Intervention: 
1. Pause new assignments (reduce from 5 to 2)
2. Send encouragement message
3. Suggest easier tasks next week
```

### Metrics the System Provides

1. **Fairness Metrics**
   - Task distribution across family
   - Matching difficulty to ability
   - Preference respect rate

2. **Engagement Metrics**
   - Completion rates (per person, trending)
   - At-risk indicators

3. **System Health**
   - Average family completion rate
   - Burnout detections
   - Motivation effectiveness

### Potential Impact

If deployed to 1 million families:
- **Time saved**: Parents spend ~2 hours/week on chore management → ~30 min automated
- **Fairness improved**: Random assignment drops to structured matching
- **Engagement**: Average completion rate increases from 65% → 80%
- **Family dynamics**: Reduced conflict over task fairness

---

## Course Concepts Applied

### 1. Multi-Agent System (ADK) ✅

**What we built:**
- Two agents: Orchestrator (assignment) + Motivator (engagement)
- Each has specialized system prompt
- Agents collaborate via shared context (JSON memory)
- Agents can be extended independently

**How it demonstrates ADK:**
- Multi-turn conversations with tool use
- Agents call tools to access real data
- Agents reason about tradeoffs
- Each agent adds value through specialization

### 2. MCP Servers ✅

**What we built:**
- 6 custom tools in `mcp_server.py`
- Each tool has proper input schema (type, description, required fields)
- Each tool returns structured data
- Tools integrate with persistent data store

**Tool Definition Example:**
```python
{
    "name": "get_engagement_metrics",
    "description": "Get engagement metrics for a family member",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "ID of the family member"
            }
        },
        "required": ["user_id"]
    }
}
```

### 3. Tool Use (Agentic Reasoning) ✅

**What we demonstrate:**
- Agents decide which tools to call and when
- Multi-turn loops: Qwen reasons, calls tools, gets results, reasons again
- Agents parse tool results and adapt behavior
- No hallucination: all facts come from tool calls, not hallucination

**Example reasoning chain:**
```
Qwen thinks: "User wants to assign chores. I need to know:
  1. What tasks are pending? → Call list_tasks()
  2. Who has capacity? → Call get_user_capacity() for each
  3. What are their preferences? → Call get_engagement_metrics()
  4. Now I can match fairly → Call assign_task()"

Result: 4 tool calls in sequence, final response based on real data
```

### 4. Security Features ✅

**What we implemented:**
- Local LLM (no data leaves your machine)
- Input validation on all tools (check task exists, user exists, etc.)
- Error messages that don't leak sensitive data
- Data isolation (each JSON file separate)

**Example validation:**
```python
# Local execution - no API keys needed
client = OpenAI(base_url="http://localhost:10000/v1", api_key="ollama")

# Input validation
if get_user(user_id) is None:
    return f"User with {user_id} Not Found"
```

### 5. Deployability ✅

**What we achieved:**
- Works locally with minimal setup (just Msty + granite4)
- Persistent memory enables offline operation
- JSON-based storage (no database needed)
- Easy to extend (add new agents, new tools)
- Clear error messages for debugging

**Quick deployment:**
```bash
# Anyone can run this:
# 1. Install Msty and download granite4
# 2. Run the script
python multi_agent_orchestrator.py
```

---

## Technical Decisions & Tradeoffs

### Why granite4 (vs. Cloud LLMs)?

✅ **Free**: No API costs, runs locally  
✅ **Private**: Family data never leaves your machine  
✅ **Fast**: Optimized for consumer GPUs  
✅ **Offline**: Works without internet  

### Why Multi-Agent (vs. Single Agent)?

✅ **Specialization**: Each agent focuses on what it's good at.  
✅ **Modularity**: Can add agents (Communicator, Analytics) without breaking existing ones.  
✅ **Reasoning**: Orchestrator doesn't need to know about motivation; Motivator doesn't need to assign.  
❌ **Complexity**: Adds 2x coordination overhead (acceptable for this use case).

### Why JSON Memory (vs. Database)?

✅ **Simple**: No database setup needed.  
✅ **Portable**: File-based, works offline.  
✅ **Human-readable**: Easy to debug and inspect.  
❌ **Scalability**: Would need database for millions of families.

### What We'd Do Differently

1. **Add Communication Agent**: SMS reminders via Twilio
2. **Add Analytics Agent**: Weekly reports for parents
3. **Persistence Layer**: Move from JSON to PostgreSQL
4. **Frontend**: Next.js app for kids/parents to see assignments
5. **Mobile**: Native mobile app with push notifications
6. **Privacy**: End-to-end encryption for family data

---

## Key Learnings from the Course

### What Worked Well

1. **Specialization**: Having agents focus on one thing made them more effective
2. **Tool Use**: Agents making decisions based on real data (not hallucination) was crucial
3. **Shared Context**: Memory system enabled agents to "understand" what the other did
4. **Clear Prompts**: Detailed system prompts with rules made agents more predictable

### Surprise Findings

1. **Motivator Agent is Complex**: Detecting at-risk members requires multi-factor analysis
2. **Memory Matters**: Agents with memory make better decisions (remember preferences)
3. **Error Handling is Critical**: Tools need validation; garbage in = garbage out
4. **User Reasoning > Output Quality**: Users trust agents more when they explain their reasoning

### If Starting Over

1. Start with single agent, prove tool calling works
2. Add second agent only after first is solid
3. Build memory system early (not as afterthought)
4. Invest in good error messages (helps with debugging)
5. Test with real family scenarios (not synthetic data)

---

## Conclusion

ChoreQuest demonstrates that AI agents excel at problems requiring:
- **Reasoning** (fairness, capacity, preferences)
- **Specialization** (different agents for different tasks)
- **Integration** (tools connecting to real data)
- **Learning** (memory system understanding preferences)

The multi-agent architecture proves effective for household coordination and could easily extend to organizations (PTOs), classrooms, or workplaces. By combining specialized agents with persistent memory and tool integration, we create systems that don't just automate tasks—they make humans' lives better.

**For families struggling with chore fairness, ChoreQuest offers intelligent, transparent coordination backed by AI reasoning.**

---

## Appendix: How to Run

### Quick Start
```bash
# 1. Install Msty (https://msty.ai)
# 2. Download granite4 model in Msty
# 3. Start Msty (runs on localhost:10000)
# 4. Run the script
python multi_agent_orchestrator.py
# Answer: "Assign all chores and celebrate achievements"
```

### Files Included
- `agent_loop.py` — Orchestrator Agent
- `motivator_agent.py` — Motivator Agent
- `multi_agent_orchestrator.py` — Main orchestrator (wires both)
- `mcp_server.py` — 6 MCP tools
- `seed_data.py` — Family data (5 members, 6 chores, 4 rewards)
- `agent_tools.py` — Tool definitions

### Expected Output
- Both agents run in sequence
- Tool calls printed to console
- Memory saved to `shared_memory.json`
- System ready for next session

---

**Word Count: ~2,400 words**  
**Course Concepts: 5/5 demonstrated** ✅  
**Track: Concierge Agents** ✅
