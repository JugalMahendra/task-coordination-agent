# Architecture Document

Task Coordination Agent - Detailed System Design

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Agent System Design](#agent-system-design)
4. [Data Flow](#data-flow)
5. [MCP Server Integration](#mcp-server-integration)
6. [Database Schema](#database-schema)
7. [API Architecture](#api-architecture)
8. [Deployment Architecture](#deployment-architecture)

---

## System Overview

The Task Coordination Agent is a distributed multi-agent system designed to coordinate tasks across two contexts (family and organization) using AI-powered reasoning and tool integration.

### **High-Level Flow**

```
User Action (Mobile/Web)
        ↓
Next.js API Route
        ↓
Agent Orchestration Layer
        ↓
Claude LLM (Tool Calling)
        ↓
MCP Servers (Database Operations, External APIs)
        ↓
Response → UI Update
```

### **Execution Models**

**Model 1: Real-time (Interactive)**
- User opens app → API route queries agent
- Agent reasons about current state
- Returns result to UI (< 2 sec)
- Example: Kid opens ChoreQuest, sees today's chores

**Model 2: Asynchronous (Batch)**
- Cron job triggers agent run (e.g., 8 AM daily)
- Agent analyzes entire dataset, makes decisions
- Writes results to database
- Sends notifications out
- Example: Morning task assignment, daily notifications

**Model 3: Event-Driven**
- User completes a task
- Event triggers motivator agent
- Agent evaluates if celebration is warranted
- Example: Kid completes 5th chore → get bonus points

---

## Core Components

### **1. Frontend Layer (Next.js)**

#### **ChoreQuest (Family Mode)**
```
chorequest/
├── app/
│   ├── layout.tsx              # Root layout with Clerk auth
│   ├── page.tsx                # Home/dashboard
│   ├── chores/
│   │   ├── [id]/page.tsx       # Chore detail view
│   │   └── actions.ts          # Server actions (claim, complete)
│   ├── dashboard/
│   │   ├── page.tsx            # Kid dashboard (tasks, points, rewards)
│   │   └── parent/page.tsx     # Parent dashboard (analytics, insights)
│   ├── api/
│   │   ├── agents/
│   │   │   ├── orchestrate.ts  # Trigger task assignment agent
│   │   │   ├── motivate.ts     # Trigger motivation agent
│   │   │   └── communicate.ts  # Send reminders
│   │   ├── chores/             # CRUD endpoints
│   │   └── rewards/            # Redemption endpoints
│   └── ...
└── lib/
    ├── prisma.ts               # Prisma client
    ├── types.ts                # TypeScript interfaces
    └── utils.ts                # Helper functions
```

#### **PTO Connect (Org Mode)**
```
pto_connect/
├── app/
│   ├── layout.tsx              # Root layout with Clerk auth
│   ├── page.tsx                # Home/dashboard
│   ├── dashboard/
│   │   ├── page.tsx            # Admin dashboard (volunteers, tasks, fundraising)
│   │   └── events/[id]/page.tsx # Event detail with task assignments
│   ├── api/
│   │   ├── agents/
│   │   │   ├── orchestrate.ts  # Volunteer assignment
│   │   │   ├── motivate.ts     # Engagement insights
│   │   │   └── communicate.ts  # Email updates
│   │   ├── volunteers/         # CRUD endpoints
│   │   └── fundraising/        # Campaign tracking
│   └── ...
└── lib/
    ├── supabase.ts             # Supabase client
    ├── types.ts                # TypeScript interfaces
    └── utils.ts                # Helper functions
```

---

### **2. Agent Orchestration Layer (Python)**

```
agents/
├── __init__.py
├── agent_loop.py               # Main orchestration loop
├── orchestrator.py             # Task assignment agent
├── engagement_motivator.py      # Motivation & tracking agent
├── communicator.py             # Reminders & updates agent
├── insights_analyzer.py        # Analytics & predictions agent
└── utils/
    ├── prompt_templates.py
    ├── tool_registry.py
    └── logging_config.py
```

#### **Agent Loop Pseudocode**

```python
async def run_agent_loop():
    """
    Main agentic loop that orchestrates multi-agent collaboration.
    Runs hourly (cron) or on-demand (API).
    """
    
    # 1. Determine context (home or org)
    context = get_execution_context()  # "home" or "organization"
    
    # 2. Fetch current state
    tasks = fetch_tasks(context)
    users = fetch_users(context)
    history = fetch_recent_history(context)
    
    # 3. Build shared context for agents
    shared_state = {
        "context": context,
        "timestamp": now(),
        "tasks": tasks,
        "users": users,
        "recent_events": history,
    }
    
    # 4. Run orchestrator agent
    orchestrator_result = await run_agent(
        agent="task_orchestrator",
        state=shared_state,
        tools=[task_coordination_mcp]
    )
    # Orchestrator decides: who should do what?
    
    # 5. Run motivation agent
    motivation_result = await run_agent(
        agent="engagement_motivator",
        state={**shared_state, "orchestrator_decisions": orchestrator_result},
        tools=[engagement_mcp, reward_engine_mcp]
    )
    # Motivator evaluates: who needs encouragement? What rewards matter?
    
    # 6. Run communication agent
    communication_result = await run_agent(
        agent="communicator",
        state={**shared_state, "orchestrator_decisions": orchestrator_result,
               "motivator_insights": motivation_result},
        tools=[communication_mcp, twilio_mcp, sendgrid_mcp]
    )
    # Communicator sends: reminders, celebrations, alerts
    
    # 7. Run insights agent
    insights_result = await run_agent(
        agent="insights_analyzer",
        state={**shared_state, ...all_previous_results...},
        tools=[analytics_mcp, forecasting_mcp]
    )
    # Insights agent generates: trends, anomalies, recommendations
    
    # 8. Log all agent decisions for audit trail
    log_agent_execution(orchestrator_result, motivation_result, 
                       communication_result, insights_result)
    
    # 9. Return results for webhook/API response
    return {
        "orchestrator": orchestrator_result,
        "motivator": motivation_result,
        "communicator": communication_result,
        "insights": insights_result,
    }
```

---

### **3. MCP Server Layer**

Four custom MCP servers expose tools to agents:

#### **Task Coordination MCP** (`mcp_servers/task_coordination/`)
```python
tools = [
    "list_tasks(context, filter_by_assignee=None, filter_by_status=None)",
    "assign_task(task_id, user_id, reason)",
    "get_user_capacity(user_id)",  # Current workload
    "detect_conflicts(assignment)",  # Can this user do this task?
    "get_assignment_history(user_id, last_n_days=30)",
]
```

#### **Engagement & Rewards MCP** (`mcp_servers/engagement_rewards/`)
```python
tools = [
    "get_engagement_metrics(user_id, time_period)",
    "list_available_rewards(context, budget=None)",
    "suggest_reward(user_id, budget_points)",
    "update_points_ledger(user_id, delta, reason)",
    "get_reward_history(user_id)",
]
```

#### **Communication MCP** (`mcp_servers/communication/`)
```python
tools = [
    "send_sms(user_id, message, scheduled_time=None)",
    "send_email(user_id, subject, template, context_vars)",
    "get_communication_preferences(user_id)",  # Preferred channel, time
    "get_opt_out_status(user_id, message_type)",
    "log_communication(user_id, channel, message, timestamp)",
]
```

#### **Insights & Analytics MCP** (`mcp_servers/insights_analytics/`)
```python
tools = [
    "get_engagement_trends(context, time_period=7_days)",
    "detect_at_risk_users(context, threshold=0.6)",  # Declining engagement
    "get_success_patterns(context)",  # What works?
    "forecast_churn(user_id)",  # Will they quit?
    "generate_report(context, type='weekly'|'monthly')",
]
```

---

## Agent System Design

### **Agent Definitions**

Each agent is configured with:
- System prompt (role, responsibilities, constraints)
- Available tools (from MCP servers)
- Context (shared state + previous agent outputs)
- Temperature (0.5-0.7 for deterministic task assignment, 0.7-0.9 for creative motivation)
- Max tokens (2000-3000 per agent run)

### **System Prompts (Examples)**

#### **Task Orchestrator System Prompt**

```
You are the Task Orchestrator Agent. Your role is to assign tasks intelligently 
across the group, considering capacity, preferences, and fairness.

Context:
- You're operating in: {{ context_mode }}  (home or organization)
- Current time: {{ timestamp }}
- Available team members: {{ user_count }}
- Pending tasks: {{ task_count }}

Your responsibilities:
1. Analyze current workloads for each person
2. Identify person-task fit (skills, preferences, past performance)
3. Suggest fair and balanced assignments
4. Detect and flag overload situations
5. Explain your reasoning for each assignment

Constraints:
- No one should be assigned more than 3 tasks per day
- Respect preferences (marked with priority_preference)
- For families: match task difficulty to age/ability
- For orgs: match skills to role requirements
- If someone is overburdened, suggest rebalancing

Available tools:
- list_tasks() - see all pending tasks
- get_user_capacity(user_id) - check current workload
- detect_conflicts(assignment) - validate assignments
- get_assignment_history() - understand past patterns
- assign_task(task_id, user_id, reason) - make assignments

Output format:
Return a JSON object with:
{
  "assignments": [
    {"task_id": "...", "user_id": "...", "confidence": 0.9, "reasoning": "..."},
    ...
  ],
  "flags": [
    {"user_id": "...", "issue": "overloaded", "recommendation": "..."},
    ...
  ]
}
```

#### **Engagement & Motivation System Prompt**

```
You are the Engagement & Motivation Agent. Your role is to understand what 
drives each person and adapt incentives to keep participation high.

Context:
- Context mode: {{ context_mode }}
- Current engagement data: {{ engagement_metrics }}
- Recent completions: {{ recent_wins }}
- At-risk users: {{ at_risk_list }}

Your responsibilities:
1. Analyze engagement trends per person
2. Identify declining participation early
3. Suggest personalized incentives (not generic)
4. Celebrate wins appropriately
5. Flag burnout risks

For families (ChoreQuest):
- What rewards actually matter to this kid? (screen time, outings, treats, badges)
- Are point values appropriate?
- Is there a pattern (avoids certain chores)?

For organizations (PTO Connect):
- What recognition matters? (public, private, impact metrics, peer recognition)
- Are volunteers feeling valued?
- Who's at risk of burning out?

Output format:
{
  "motivations": {
    "user_id": {
      "current_engagement": 0.7,
      "trend": "declining",
      "effective_incentives": ["recognition", "flexible_hours"],
      "suggested_action": "..."
    }
  },
  "at_risk": [
    {"user_id": "...", "reason": "no activity in 7 days", "intervention": "..."}
  ]
}
```

---

## Data Flow

### **Scenario: Task Assignment → Notification → Celebration**

```
[1] USER ACTION (Mobile/Web)
    └─ Kid opens ChoreQuest app
       
[2] API ROUTE TRIGGERED
    └─ GET /api/agents/orchestrate?context=home
    
[3] ORCHESTRATOR AGENT RUNS
    └─ Fetches: pending tasks, kid's capacity, preferences
    └─ Calls: list_tasks(), get_user_capacity(), assign_task()
    └─ Decides: "Emma should do 'wash dishes' (high points, she's good at this)"
    └─ Returns: assignment decision
    
[4] ENGAGEMENT AGENT EVALUATES
    └─ Analyzes Emma's history: "She avoids dishes but completes them 90% of the time"
    └─ Suggests: bonus points to motivate
    └─ Returns: motivation strategy
    
[5] COMMUNICATION AGENT SENDS REMINDER
    └─ Checks preference: Emma prefers push notification over SMS
    └─ Scheduled time: 6 PM (when she usually checks app)
    └─ Message: "Dish duty! 50 points + 10 bonus if done by 8 PM 🎯"
    
[6] KID COMPLETES TASK
    └─ POST /api/chores/[id]/complete
    └─ Triggers motivation agent again (async)
    
[7] MOTIVATION AGENT CELEBRATES
    └─ "Emma completed dishes! She's on a 5-day streak 🎉"
    └─ Suggests reward: "She's earned enough for 30 min YouTube"
    └─ Calls update_points_ledger() to credit points
    
[8] INSIGHTS AGENT LOGS PATTERN
    └─ "Bonus points work for this kid. Keep using them."
    └─ Updates forecasting model
    
[9] UI UPDATES
    └─ Points increased
    └─ Celebration animation
    └─ Reward eligibility updated
```

---

## MCP Server Integration

### **How Agents Call MCP Tools**

```
Agent (Claude) --[tool_call]--> MCP Server --[function call]--> Database/API
    ↑                                                                    ↓
    └────────────────── [tool_result] ←──────────────────────────────┘
```

### **Example: Agent Calls assign_task()**

```json
{
  "type": "tool_use",
  "id": "toolu_01...",
  "name": "assign_task",
  "input": {
    "task_id": "task_123",
    "user_id": "user_456",
    "reason": "Emma has completed 3 dishes tasks this month with 95% success rate. This task aligns with her preferences and capacity."
  }
}
```

MCP Server Response:
```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01...",
  "content": {
    "success": true,
    "assignment_id": "assign_789",
    "task": {
      "id": "task_123",
      "title": "Wash dishes",
      "points": 50
    },
    "user": {
      "id": "user_456",
      "name": "Emma"
    },
    "assigned_at": "2026-06-24T14:30:00Z"
  }
}
```

---

## Database Schema

### **ChoreQuest (Prisma + Neon)**

```prisma
model User {
  id            String    @id @default(cuid())
  clerkId       String    @unique
  name          String
  email         String    @unique
  role          String    // "parent" or "child"
  age           Int?
  createdAt     DateTime  @default(now())
  
  // Relationships
  tasks         Task[]
  completions   TaskCompletion[]
  rewards       Reward[]
  pointsLedger  PointsLedger[]
}

model Task {
  id            String    @id @default(cuid())
  title         String
  description   String?
  points        Int
  difficulty    String    // "easy", "medium", "hard"
  dueDate       DateTime?
  status        String    // "pending", "assigned", "completed", "overdue"
  
  assignedTo    User?     @relation(fields: [assignedUserId], references: [id])
  assignedUserId String?
  createdBy     User      @relation(fields: [createdById], references: [id])
  createdById   String
  
  completions   TaskCompletion[]
  agentNotes    String?   // "Emma avoids this, avoid assigning"
  
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model TaskCompletion {
  id            String    @id @default(cuid())
  task          Task      @relation(fields: [taskId], references: [id])
  taskId        String
  user          User      @relation(fields: [userId], references: [id])
  userId        String
  
  completedAt   DateTime
  pointsAwarded Int
  bonusPoints   Int       @default(0)  // From motivation agent
  
  createdAt     DateTime  @default(now())
}

model PointsLedger {
  id            String    @id @default(cuid())
  user          User      @relation(fields: [userId], references: [id])
  userId        String
  
  delta         Int       // +50, -10, etc.
  reason        String    // "task_completion", "reward_redemption", "bonus"
  metadata      Json?     // { "task_id": "...", "agent_action": "bonus_motivation" }
  
  createdAt     DateTime  @default(now())
}

model Reward {
  id            String    @id @default(cuid())
  title         String
  description   String
  cost          Int       // points required
  category      String    // "screen_time", "activity", "treat", "badge"
  
  redemptions   RewardRedemption[]
  createdAt     DateTime  @default(now())
}

model RewardRedemption {
  id            String    @id @default(cuid())
  reward        Reward    @relation(fields: [rewardId], references: [id])
  rewardId      String
  user          User      @relation(fields: [userId], references: [id])
  userId        String
  
  redeemedAt    DateTime
  expiresAt     DateTime? // For screen-time rewards
  
  createdAt     DateTime  @default(now())
}
```

### **PTO Connect (Supabase)**

Similar structure but adapted for org context:
- `User` → `Volunteer`
- `Task` → `VolunteerRole` / `Event`
- `Points` → `ImpactScore` (hours, funds raised, etc.)
- `Reward` → `Recognition` (badges, public mentions)

---

## API Architecture

### **Vercel Serverless Functions**

```
chorequest/app/api/
├── agents/
│   ├── orchestrate.ts   # POST /api/agents/orchestrate
│   ├── motivate.ts      # POST /api/agents/motivate
│   └── communicate.ts   # POST /api/agents/communicate
├── chores/
│   ├── route.ts         # GET (list), POST (create)
│   └── [id]/route.ts    # GET, PATCH, DELETE
└── tasks/
    └── [id]/complete.ts # POST (mark complete)
```

### **Example: POST /api/agents/orchestrate**

**Request:**
```json
{
  "context": "home",
  "trigger": "daily_assignment"  // or "on_demand"
}
```

**Response:**
```json
{
  "status": "success",
  "execution_id": "exec_abc123",
  "assignments": [
    {
      "task_id": "task_1",
      "user_id": "user_1",
      "confidence": 0.92,
      "reasoning": "Emma has high success rate with dishes..."
    }
  ],
  "notifications_sent": 3,
  "execution_time_ms": 1250
}
```

---

## Deployment Architecture

### **Components & Hosting**

```
┌─ Vercel (Frontend + Agents) ──────────────────────────┐
│                                                       │
│  chorequest.vercel.app/                              │
│  ├── Next.js app (Node.js runtime)                   │
│  ├── Serverless functions (/api/agents/...)          │
│  └── Agent Python execution (via containerized proc) │
│                                                       │
│  pto-connect.vercel.app/                             │
│  ├── Next.js app (Node.js runtime)                   │
│  ├── Serverless functions (/api/agents/...)          │
│  └── Agent Python execution (via containerized proc) │
│                                                       │
└───────────────────────────────────────────────────────┘

┌─ Docker (MCP Servers) ────────────────────────────────┐
│                                                       │
│  mcp-task-coordination:5001                          │
│  mcp-engagement-rewards:5002                         │
│  mcp-communication:5003                              │
│  mcp-insights-analytics:5004                         │
│                                                       │
│  (Deployed to Cloud Run, ECS, or self-hosted)       │
│                                                       │
└───────────────────────────────────────────────────────┘

┌─ Databases ───────────────────────────────────────────┐
│                                                       │
│  Neon (PostgreSQL) ← ChoreQuest                       │
│  Supabase (PostgreSQL) ← PTO Connect                  │
│                                                       │
└───────────────────────────────────────────────────────┘

┌─ External Services ───────────────────────────────────┐
│                                                       │
│  Anthropic API ← Claude (agent reasoning)            │
│  Twilio ← SMS notifications                          │
│  SendGrid ← Email notifications                      │
│  Stripe ← Fundraising (PTO mode)                    │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## Summary

This architecture enables:
- ✅ **Intelligent decision-making** via Claude + tool use
- ✅ **Modularity** via MCP servers
- ✅ **Scalability** via serverless functions
- ✅ **Dual-mode operation** (home + org) from single codebase
- ✅ **Auditability** via logging of all agent decisions
- ✅ **Extensibility** via pluggable MCP servers

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup details.
