# Multi-Agent Marketing Campaign System

A multi-agent AI system built with **LangChain + FastAPI** (Python) and **Angular** that demonstrates intelligent agent collaboration on a real-world marketing workflow. Four specialized agents work sequentially, with a critic-driven feedback loop, streaming results to the frontend in real time.

> **Free to run** — powered by [Groq](https://console.groq.com) (LLaMA 3.3 70B). No credit card required.

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Angular Frontend                   │
│          Campaign Brief Form  ·  Live Agent Feed      │
└─────────────────────┬────────────────────────────────┘
                      │  HTTP POST + Server-Sent Events
┌─────────────────────▼────────────────────────────────┐
│              FastAPI Orchestration Layer              │
│       Coordinates agents · Streams SSE events        │
└──┬─────────────┬──────────────┬──────────────┬───────┘
   │             │              │              │
┌──▼──────┐ ┌───▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
│Research │ │Sentiment │ │  Content  │ │  Critic   │
│ Agent   │ │  Agent   │ │  Agent   │ │  Agent    │
│         │ │          │ │           │ │           │
│Retrieves│ │ Audience │ │ Generates │ │ Scores &  │
│ market  │ │ mood map │ │  campaign │ │ validates │
│ context │ │& triggers│ │   copy    │ │  output   │
└─────────┘ └──────────┘ └─────┬─────┘ └─────┬─────┘
                                │             │
                                └─ revision ──┘
                                  (score < 7/10)
```

### Agent Responsibilities

| Agent | Responsibility | Output |
|---|---|---|
| **Research Agent** | Synthesizes market intelligence, competitors, and key facts | `ResearchBrief` |
| **Sentiment Agent** | Maps audience emotional landscape and pain points | `SentimentReport` |
| **Content Agent** | Generates tagline, email copy, and social posts | `CampaignContent` |
| **Critic Agent** | Scores content on 5 criteria; triggers revision if score < 7/10 | `CriticReview` |

### Orchestration Pattern

- **Sequential pipeline with feedback loop**: Research → Sentiment → Content → Critic → *(optional revision)*
- Each agent receives strongly-typed Pydantic outputs from prior agents as context
- The Critic enforces a **quality gate**: if `overall_score < 7.0`, it sends specific revision notes back to the Content Agent for one revision pass
- All agent steps stream to the frontend in real time via **Server-Sent Events (SSE)**

### Data Flow

```
CampaignRequest
    → [tools] market_data + audience_insights
    → ResearchBrief
    → [tools] content_performance
    → SentimentReport
    → CampaignContent
    → CriticReview
        → (if not approved) CampaignContent (revised)
        → (final) CriticReview
    → CampaignResult (streamed to frontend)
```

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| LLM | **Groq** — LLaMA 3.3 70B | Free inference API |
| Agent Framework | **LangChain** | Tool wrappers, message types |
| Backend | **FastAPI** + Python 3.11 | Async, SSE streaming |
| Data Validation | **Pydantic v2** | Typed contracts between agents |
| Streaming | **sse-starlette** | Real-time event delivery |
| Frontend | **Angular 17** | Standalone components, SSE consumer |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com) (no credit card required)

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Open .env and set GROQ_API_KEY=<your_key>

# Start the API server
uvicorn api.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
ng serve
# Open http://localhost:4200
```

---

## Project Structure

```
multi-agent-system/
├── backend/
│   ├── agents/
│   │   ├── research_agent.py     # Market intelligence synthesis
│   │   ├── sentiment_agent.py    # Audience emotional analysis
│   │   ├── content_agent.py      # Campaign copy generation
│   │   └── critic_agent.py       # Quality gate + revision feedback
│   ├── api/
│   │   └── main.py               # FastAPI orchestrator + SSE streaming
│   ├── models/
│   │   └── schemas.py            # Pydantic schemas (agent data contracts)
│   ├── tools/
│   │   └── mock_tools.py         # Tool layer (swappable for real APIs)
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    └── src/app/
        ├── components/
        │   ├── campaign-form/     # Campaign brief input
        │   ├── agent-feed/        # Real-time agent activity log
        │   └── results-panel/     # Final campaign output display
        ├── services/
        │   └── campaign.service.ts  # SSE consumer
        └── models/
            └── campaign.models.ts   # TypeScript interfaces
```

---

## Design Decisions

**1. Single-responsibility agents**
Each agent has one job, one focused system prompt, and one typed output schema. This makes individual agents testable, replaceable, and upgradeable in isolation — the same principle as microservices applied to LLM agents.

**2. Typed data contracts between agents**
Every agent input and output is a Pydantic model. Agents cannot pass free-form text to each other; data is validated at every boundary. This prevents error propagation and makes the system predictable.

**3. Critic-driven feedback loop**
The Critic agent introduces a quality gate rather than pass-through. If content scores below 7/10, it generates specific, actionable revision notes and routes back to the Content Agent. This is what distinguishes a multi-agent *collaboration* from a simple chain.

**4. Real-time SSE streaming**
Rather than blocking until the full pipeline completes (which takes 15–30 seconds), the backend streams each agent's status and output to the frontend as it happens, providing a live view of the pipeline execution.

**5. Swappable tool layer**
The `tools/` module uses LangChain `@tool` wrappers with mock data. Replacing any tool with a real API (SerpAPI, Google Trends, HubSpot Analytics) requires only a change to the tool implementation — no agent code changes needed.

---

## Groq Free Tier

| Metric | Limit |
|---|---|
| Requests / minute | 30 |
| Tokens / minute | 14,400 |
| Requests / day | 14,400 |
| Cost | **$0** |

Each pipeline run makes ~4–6 LLM calls and completes in approximately 15–30 seconds depending on model load.

---

## Example Run

**Input**

| Field | Value |
|---|---|
| Topic | Sustainable Coffee Pods |
| Target Audience | Eco-conscious millennials |
| Tone | Inspiring |
| Goal | Brand Awareness |

**Output**

- `ResearchBrief` — market context, key facts, competitor landscape, opportunities
- `SentimentReport` — overall mood, pain points, emotional triggers, trend score
- `CampaignContent` — tagline, email subject + body, 3 social posts (Instagram / Twitter / LinkedIn), CTA
- `CriticReview` — overall score /10, strengths, weaknesses, approval status

If the Critic scores below 7/10, a revision cycle is triggered automatically and the final output reflects the improved version.

---

## Extending the System

The architecture is designed to be extended:

- **Add a new agent** — create a new file in `agents/`, define its Pydantic output schema, and wire it into the orchestrator
- **Connect real tools** — replace mock implementations in `tools/mock_tools.py` with SerpAPI, SparkToro, Mailchimp, etc.
- **Add memory** — inject `ConversationBufferMemory` to allow agents to reference previous campaign runs
- **Parallel agents** — Research and Sentiment could run concurrently with `asyncio.gather()` since they don't depend on each other
