# Task Coordination Agent

An intelligent multi-agent AI system for coordinating tasks, tracking engagement, and motivating participation across both family and organizational contexts.

**Kaggle Capstone Project:** AI Agents: Intensive Vibe Coding Course with Google

---

## 🎯 Problem Statement

Task coordination and motivation are hard—whether you're managing family chores or organizing PTO (Parent Teacher Organization) volunteers. Both contexts face similar challenges:

### **In Families (ChoreQuest)**
- Kids forget or avoid chores; parents manually remind them
- No clear picture of who's overloaded vs. underutilized
- Reward systems feel disconnected or generic
- Parents spend time enforcing, not celebrating progress

### **In Organizations (PTO Connect)**
- Volunteers burn out because workload is unbalanced
- Admin staff manually coordinate task assignments and track RSVPs
- No intelligent matching between member skills and needs
- Engagement metrics are opaque (hard to know who's at risk of leaving)

**Core insight:** Both problems are fundamentally the same—intelligent task coordination with adaptive motivation.

---

## 💡 Solution: Unified Task Coordination Agent

A **multi-agent AI system** that learns your context (family or organization), understands individual preferences and capabilities, and automatically:

1. **Assigns tasks intelligently** — matching people to roles they're likely to succeed at
2. **Tracks engagement** — identifies who's overloaded, underutilized, or at risk of burnout
3. **Motivates participation** — offers incentives tailored to what actually drives each person
4. **Communicates proactively** — sends reminders, celebrates wins, alerts leaders to issues
5. **Provides insights** — analyzes patterns, flags risks, suggests improvements

### **Key Innovation**

A single intelligent agent framework that **adapts to context**:
- Same core agents (Orchestrator, Motivator, Communicator, Insights)
- Different data sources (Prisma for home, Supabase for org)
- Different UI layers (child-friendly vs. admin-focused)
- Same reasoning engine (Claude via API)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│          Task Coordination Agent Framework              │
│           (Multi-Agent System Core - Claude)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  ChoreQuest      │  │   PTO Connect    │            │
│  │  (Home Mode)     │  │   (Org Mode)     │            │
│  ├──────────────────┤  ├──────────────────┤            │
│  │ UI Layer         │  │ UI Layer         │            │
│  │ (Vercel/Next.js) │  │ (Vercel/Next.js) │            │
│  └────────┬─────────┘  └────────┬─────────┘            │
│           │                     │                      │
│           └─────────────────────┘                      │
│                     │                                  │
│  ┌──────────────────────────────────────┐             │
│  │     Agent Orchestration Layer        │             │
│  │  (Agentic Loop / Tool Use)           │             │
│  ├──────────────────────────────────────┤             │
│  │ • Task Orchestrator Agent            │             │
│  │ • Engagement & Motivation Agent      │             │
│  │ • Communication & Reminder Agent     │             │
│  │ • Insight & Analytics Agent          │             │
│  └──────────────────────────────────────┘             │
│           │              │              │              │
│  ┌────────┴──┐  ┌────────┴──┐  ┌───────┴──────┐      │
│  │ MCP Task  │  │ MCP Eng.  │  │ MCP Comms    │      │
│  │ Coord.    │  │ & Reward  │  │ & Reminders  │      │
│  │ Server    │  │ Server    │  │ Server       │      │
│  └────┬──────┘  └────┬──────┘  └───────┬──────┘      │
│       │              │                 │              │
│   ┌───┴────────┬─────┴──────┬──────────┴───┐         │
│   │            │            │              │         │
│  [DB]       [DB]         [APIs]          [DB]        │
│ Prisma    Supabase   Twilio/SendGrid   Supabase     │
│ (Home)     (Org)      (Comms)          (Insights)   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### **The Four Core Agents**

#### **1. Task Orchestrator Agent**
- **Role:** Intelligent task assignment and scheduling
- **Home mode:** Analyzes family dynamics, suggests chore rotations based on age/ability/preferences
- **Org mode:** Optimizes volunteer scheduling, balances committee workload
- **Tools:** Task coordination MCP server (reads/writes tasks, detects conflicts)

**Example prompt:**
```
You are a Task Orchestrator for a family/organization. Your goal is to assign tasks 
fairly and intelligently, considering:
- Individual capacity (who's overloaded right now?)
- Preferences (what does each person enjoy?)
- Skills (who's best suited for this task?)
- History (what have they been assigned recently?)

Given the current task list and team state, suggest optimal assignments.
```

---

#### **2. Engagement & Motivation Agent**
- **Role:** Tracks participation and adapts incentives
- **Home mode:** Manages point economy, suggests personalized rewards (screen time, outings, treats)
- **Org mode:** Highlights contributions, calculates impact metrics, suggests peer recognition
- **Tools:** Engagement & reward MCP server, analytics

**Example prompt:**
```
You are an Engagement Agent managing motivation across the group. Your goal is to 
understand what actually drives each person and suggest incentives they'll value.

Analyze participation history and engagement patterns. For declining engagement, 
recommend interventions (adjust task difficulty, change incentives, offer recognition).
```

---

#### **3. Communication & Reminder Agent**
- **Role:** Proactive, contextual communication
- **Channels:** SMS (Twilio), Email (SendGrid), In-app push
- **Smart timing:** Learns when each person is most likely to check messages
- **Personalization:** Different tone for kids vs. parents/admins
- **Tools:** Communication MCP server (Twilio, SendGrid integration)

**Example prompt:**
```
You are a Communication Agent. Send timely, personalized reminders and updates.

For reminders: Use the person's preferred channel and time. Keep tone encouraging.
For updates: Celebrate wins. Alert leaders to issues early.
For motivational messages: Reference past successes to build momentum.
```

---

#### **4. Insight & Analytics Agent**
- **Role:** Discovers patterns and flags risks
- **Home mode:** "Emma loves outdoor tasks," "Friday is pizza night—avoid task deadlines," "Completion rate trending down"
- **Org mode:** "Fundraising committee engagement is 40% down YoY," "Top volunteer hours by role," "Retention risk: Sarah hasn't engaged in 3 weeks"
- **Tools:** Analytics MCP server, data warehouse

**Example prompt:**
```
You are an Insights Agent. Analyze historical data to discover patterns and flag risks.

Generate a weekly/monthly report covering:
- Engagement trends
- Anomalies (drops, spikes)
- At-risk individuals
- Success stories (to replicate)
- Recommendations for leaders
```

---

## 🛠️ Tech Stack

### **Frontend**
- **Framework:** Next.js 14+ (TypeScript)
- **Styling:** Tailwind CSS + shadcn/ui
- **Deployment:** Vercel
- **Authentication:** Clerk

### **Database & Backend**
- **Home (ChoreQuest):** Prisma ORM + Neon (PostgreSQL)
- **Org (PTO Connect):** Supabase (PostgreSQL)
- **Real-time:** Supabase realtime (for org), webhook polling (for home)

### **AI & Agents**
- **LLM:** Claude 3.5 Sonnet (via Anthropic API)
- **Agent Framework:** Custom agentic loop (Claude tool_use)
- **MCP Servers:** 4 custom servers (TypeScript/Python)
  - `mcp-task-coordination`
  - `mcp-engagement-rewards`
  - `mcp-communication`
  - `mcp-insights-analytics`

### **External APIs**
- **Twilio:** SMS reminders
- **SendGrid:** Email notifications
- **Stripe Connect:** Fundraising tracking (PTO mode)

### **Deployment**
- **Agents:** Vercel serverless functions (Node.js)
- **MCP Servers:** Docker containers (or Vercel with constraints)
- **Cron Jobs:** Trigger agent runs hourly/daily (Vercel cron or external scheduler)

---

## 📂 Repository Structure

```
task-coordination-agent/
├── LICENSE
├── README.md
├── .gitignore
├── .env.example
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py          # Task assignment logic
│   ├── engagement_motivator.py   # Motivation & tracking
│   ├── communicator.py           # SMS/email/push
│   ├── insights_analyzer.py      # Analytics & predictions
│   └── agent_loop.py             # Main agentic loop
│
├── mcp_servers/
│   ├── task_coordination/
│   │   ├── server.py
│   │   └── tools.py
│   ├── engagement_rewards/
│   │   ├── server.py
│   │   └── tools.py
│   ├── communication/
│   │   ├── server.py
│   │   └── tools.py (Twilio, SendGrid)
│   └── insights_analytics/
│       ├── server.py
│       └── tools.py
│
├── chorequest/                   # Family chore app
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   ├── api/
│   │   │   └── agents/
│   │   │       ├── orchestrate.ts
│   │   │       ├── motivate.ts
│   │   │       └── communicate.ts
│   │   └── ...
│   ├── lib/
│   │   ├── prisma.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   ├── prisma/
│   │   └── schema.prisma
│   ├── public/
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── pto_connect/                  # Organization volunteer app
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   ├── api/
│   │   │   └── agents/
│   │   │       ├── orchestrate.ts
│   │   │       ├── motivate.ts
│   │   │       └── communicate.ts
│   │   └── ...
│   ├── lib/
│   │   ├── supabase.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   ├── public/
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/
│   ├── ARCHITECTURE.md            # Detailed architecture
│   ├── AGENT_PROMPTS.md           # Agent system prompts
│   ├── API_CONTRACTS.md           # API specifications
│   ├── DEPLOYMENT.md              # How to deploy
│   ├── MCP_SERVERS.md             # MCP server setup
│   └── diagrams/
│       └── architecture.svg
│
├── docker/
│   ├── Dockerfile                 # For MCP servers
│   └── docker-compose.yml
│
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_mcp_servers.py
│   └── test_orchestration.py
│
└── scripts/
    ├── setup_local.sh
    ├── deploy_agents.sh
    └── seed_demo_data.py
```

---

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon, Supabase)
- Anthropic API key
- Twilio account (for SMS)
- SendGrid account (for email)

### **Local Setup**

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/task-coordination-agent.git
   cd task-coordination-agent
   ```

2. **Install dependencies:**
   ```bash
   # Frontend (ChoreQuest)
   cd chorequest
   npm install
   
   # Frontend (PTO Connect)
   cd ../pto_connect
   npm install
   
   # Agents (Python)
   cd ..
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # Copy example env file
   cp .env.example .env.local
   
   # Edit and add your API keys:
   # ANTHROPIC_API_KEY=sk-xxx
   # TWILIO_ACCOUNT_SID=xxx
   # SENDGRID_API_KEY=xxx
   # DATABASE_URL=postgresql://...
   # SUPABASE_URL=https://xxx.supabase.co
   # SUPABASE_KEY=xxx
   ```

4. **Setup databases:**
   ```bash
   # ChoreQuest (Neon/Prisma)
   cd chorequest
   npx prisma migrate dev --name init
   
   # PTO Connect uses Supabase (schema at: pto_connect/lib/schema.sql)
   ```

5. **Start MCP servers (in separate terminals):**
   ```bash
   python mcp_servers/task_coordination/server.py
   python mcp_servers/engagement_rewards/server.py
   python mcp_servers/communication/server.py
   python mcp_servers/insights_analytics/server.py
   ```

6. **Start agent loop (in separate terminal):**
   ```bash
   python agents/agent_loop.py
   ```

7. **Start frontend apps (in separate terminals):**
   ```bash
   # ChoreQuest
   cd chorequest
   npm run dev  # http://localhost:3000
   
   # PTO Connect
   cd ../pto_connect
   npm run dev  # http://localhost:3001
   ```

### **Demo**

- **ChoreQuest:** http://localhost:3000 (Log in with demo account: kid@demo.local / password)
- **PTO Connect:** http://localhost:3001 (Log in with demo account: admin@demo.local / password)

---

## 📊 Key Features

### **ChoreQuest (Family Mode)**
- ✅ Intelligent chore assignment based on preferences & capacity
- ✅ Points system with redemable rewards
- ✅ SMS reminders to kids (via Twilio)
- ✅ Parent dashboard with engagement insights
- ✅ Kid-friendly mobile UI (pastel neon dark mode)
- ✅ Weekly rewards reset

### **PTO Connect (Org Mode)**
- ✅ Volunteer coordinator dashboard
- ✅ Intelligent task assignment to members
- ✅ Fundraising tracking & goal visualization
- ✅ Email updates & celebration notifications
- ✅ Impact metrics & contribution highlights
- ✅ At-risk volunteer detection

### **Shared Agent Capabilities**
- ✅ **Multi-agent orchestration** (4 specialized agents collaborate)
- ✅ **MCP server integration** (4 custom servers for tools)
- ✅ **Tool use** (agents reason about when/how to use tools)
- ✅ **Context awareness** (learns preferences over time)
- ✅ **Proactive communication** (reaches out, doesn't wait to be asked)
- ✅ **Security** (encrypted data, no API key exposure)

---

## 🧠 AI/Agent Concepts Applied

This project demonstrates the following concepts from the Kaggle course:

| Concept | Implementation |
|---------|-----------------|
| **Agent / Multi-agent System** | 4 agents (Orchestrator, Motivator, Communicator, Insights) collaborate via shared context |
| **MCP Servers** | 4 custom MCP servers expose tools for task management, rewards, communication, analytics |
| **Tool Use** | Agents reason about which tools to call and in what order (e.g., "Get tasks → Analyze engagement → Send reminder") |
| **Security** | API keys in environment variables, encrypted family data in DB, audit logging for all agent actions |
| **Deployability** | Live on Vercel (serverless), MCP servers containerized, full setup instructions in docs |
| **Agent Skills (CLI)** | `agents/` directory contains Python scripts; can be invoked from CLI or as API endpoints |

---

## 🔐 Security Considerations

### **Data Privacy**
- ✅ Family data (ChoreQuest) encrypted at rest in Neon
- ✅ Org data (PTO Connect) encrypted at rest in Supabase
- ✅ PII (names, emails) hashed in analytics
- ✅ Demo data does not include real personal information

### **API Key Management**
- ✅ All keys in `.env.local` (not committed)
- ✅ Environment variable validation on startup
- ✅ No hardcoded API keys or secrets in code
- ✅ Anthropic API requests include rate limiting

### **Agent Oversight**
- ✅ All agent actions logged (agent_id, timestamp, action, tool_used)
- ✅ Admin can review agent decisions before they're executed
- ✅ Agents have max_tokens limit (prevent runaway API costs)
- ✅ User opt-out for automated reminders

---

## 📈 Deployment

### **Production Deployment**

See `docs/DEPLOYMENT.md` for detailed instructions on deploying to:
- Vercel (frontend + serverless agents)
- Docker (MCP servers)
- Neon/Supabase (databases)

**Quick summary:**
```bash
# Deploy frontend
vercel --prod

# Deploy agents (Vercel functions)
# Configured in chorequest/vercel.json and pto_connect/vercel.json

# Deploy MCP servers (Docker)
docker build -t task-coordination-mcp .
docker run -e ANTHROPIC_API_KEY=xxx task-coordination-mcp
```

---

## 📝 Documentation

- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — Detailed system design, data flows, agent collaboration
- **[AGENT_PROMPTS.md](dist/AGENT_PROMPTS.md)** — System prompts, tool descriptions, example interactions
- **[API_CONTRACTS.md](./docs/API_CONTRACTS.md)** — API endpoint specifications, request/response schemas
- **[MCP_SERVERS.md](./docs/MCP_SERVERS.md)** — How to run MCP servers locally and in production
- **[DEPLOYMENT.md](./docs/DEPLOYMENT.md)** — Step-by-step deployment guide

---

## 🧪 Testing

```bash
# Run agent tests
pytest tests/test_agents.py -v

# Run MCP server tests
pytest tests/test_mcp_servers.py -v

# Test orchestration end-to-end
pytest tests/test_orchestration.py -v

# Load test agents
pytest tests/test_agents.py --load -n 10
```

---

## 🤝 Contributing

This is a capstone project. For bugs or improvements, please open an issue.

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) file for details.

This project uses open source libraries and code. All dependencies are OSI-approved.

---

## 👤 Author

**Jugal** — Technology Lead & Senior Java Engineer  
Building AI-powered SaaS products  
[LinkedIn](https://linkedin.com/in/jugal) | [GitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Kaggle & Google** for the AI Agents course and capstone opportunity
- **Anthropic** for Claude API and agent documentation
- **Open source community** for amazing libraries (Next.js, Prisma, FastAPI, etc.)

---

## 📞 Support

For questions about this project:
- 📧 Email: your.email@example.com
- 💬 GitHub Issues: [Open an issue](https://github.com/yourusername/task-coordination-agent/issues)
- 📖 Kaggle Writeup: [Link to your submission]

---

**Last Updated:** June 24, 2026  
**Status:** Active development for Kaggle Capstone (Deadline: July 6, 2026)
