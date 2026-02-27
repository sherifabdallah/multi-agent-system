"""
FastAPI Orchestration Layer
Coordinates all agents and streams events to the frontend via SSE.
Uses Groq (FREE) as the LLM provider — get your key at https://console.groq.com
"""
import asyncio
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from sse_starlette.sse import EventSourceResponse

from agents.content_agent import run_content_agent
from agents.critic_agent import run_critic_agent
from agents.research_agent import run_research_agent
from agents.sentiment_agent import run_sentiment_agent
from models.schemas import AgentEvent, AgentName, CampaignRequest
from tools.mock_tools import (
    analyze_content_performance,
    get_audience_insights,
    search_market_data,
)

load_dotenv()

app = FastAPI(title="Multi-Agent Marketing System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_REVISIONS = 1  # Critic can trigger at most 1 revision cycle

# ── Groq model options (all FREE) ────────────────────────────────────────────
# "llama3-70b-8192"    → Best quality, recommended
# "llama3-8b-8192"     → Faster, still great
# "mixtral-8x7b-32768" → Good alternative
GROQ_MODEL = "llama-3.3-70b-versatile"

def get_llm() -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


async def orchestrate_campaign(request: CampaignRequest) -> AsyncGenerator[str, None]:
    """
    Main orchestration coroutine.
    Runs agents sequentially, yielding SSE events at each step.
    Pattern: Research → Sentiment → Content → Critic → (optional revision)
    """
    llm = get_llm()

    def emit(agent: AgentName, status: str, message: str, data: dict = None) -> str:
        event = AgentEvent(agent=agent, status=status, message=message, data=data)
        return event.model_dump_json()

    # ── Step 1: Tool calls ───────────────────────────────────────────────────
    yield emit(AgentName.ORCHESTRATOR, "thinking", "Initializing multi-agent pipeline...")
    await asyncio.sleep(0.3)

    yield emit(AgentName.RESEARCH, "thinking", f"Searching market data for '{request.topic}'...")
    await asyncio.sleep(0.4)
    market_data = search_market_data.invoke({"topic": request.topic})

    yield emit(AgentName.RESEARCH, "thinking", f"Gathering audience insights for '{request.target_audience}'...")
    await asyncio.sleep(0.3)
    audience_data = get_audience_insights.invoke({"audience": request.target_audience})

    # ── Step 2: Research Agent ───────────────────────────────────────────────
    yield emit(AgentName.RESEARCH, "thinking", "Synthesizing research brief with LLaMA 3...")
    research = await run_research_agent(request, llm, market_data, audience_data)
    yield emit(
        AgentName.RESEARCH,
        "done",
        f"Research complete. Found {len(research.key_facts)} key facts and {len(research.opportunities)} opportunities.",
        research.model_dump(),
    )
    await asyncio.sleep(0.2)

    # ── Step 3: Sentiment Agent ──────────────────────────────────────────────
    yield emit(AgentName.SENTIMENT, "thinking", "Analyzing audience sentiment and emotional landscape...")
    performance_data = analyze_content_performance.invoke(
        {"tone": request.tone, "content_type": "email campaign"}
    )
    sentiment = await run_sentiment_agent(request, research, llm, audience_data, performance_data)
    yield emit(
        AgentName.SENTIMENT,
        "done",
        f"Sentiment analysis complete. Trend score: {sentiment.trend_score}/10. Angle: {sentiment.recommended_angle[:60]}...",
        sentiment.model_dump(),
    )
    await asyncio.sleep(0.2)

    # ── Step 4: Content Agent ────────────────────────────────────────────────
    yield emit(AgentName.CONTENT, "thinking", "Generating campaign content package...")
    content = await run_content_agent(request, research, sentiment, llm)
    yield emit(
        AgentName.CONTENT,
        "done",
        f"Content generated. Tagline: '{content.tagline}'",
        content.model_dump(),
    )
    await asyncio.sleep(0.2)

    # ── Step 5: Critic Agent ─────────────────────────────────────────────────
    yield emit(AgentName.CRITIC, "thinking", "Reviewing content against campaign criteria...")
    review = await run_critic_agent(request, content, sentiment, llm, iteration=1)
    yield emit(
        AgentName.CRITIC,
        "done" if review.approved else "thinking",
        f"Review complete. Score: {review.overall_score}/10. {'✅ Approved!' if review.approved else '⚠️ Requesting revision...'}",
        review.model_dump(),
    )

    # ── Step 6: Optional Revision Loop ──────────────────────────────────────
    revised_content = None
    total_iterations = 1

    if not review.approved and MAX_REVISIONS > 0:
        total_iterations = 2
        yield emit(
            AgentName.CONTENT,
            "thinking",
            f"Revising content based on critic feedback: {review.revision_notes[:80]}...",
        )
        revised_content = await run_content_agent(
            request, research, sentiment, llm, revision_notes=review.revision_notes
        )
        yield emit(
            AgentName.CONTENT,
            "done",
            f"Revision complete. New tagline: '{revised_content.tagline}'",
            revised_content.model_dump(),
        )

        yield emit(AgentName.CRITIC, "thinking", "Re-reviewing revised content...")
        final_review = await run_critic_agent(
            request, revised_content, sentiment, llm, iteration=2
        )
        review = final_review
        yield emit(
            AgentName.CRITIC,
            "done",
            f"Final review: {review.overall_score}/10. {'✅ Approved!' if review.approved else 'Accepted as best effort.'}",
            review.model_dump(),
        )

    # ── Step 7: Final result ─────────────────────────────────────────────────
    final_result = {
        "request": request.model_dump(),
        "research": research.model_dump(),
        "sentiment": sentiment.model_dump(),
        "content": (revised_content or content).model_dump(),
        "original_content": content.model_dump() if revised_content else None,
        "review": review.model_dump(),
        "total_iterations": total_iterations,
    }

    yield emit(
        AgentName.ORCHESTRATOR,
        "done",
        f"Pipeline complete in {total_iterations} iteration(s). Final score: {review.overall_score}/10.",
        final_result,
    )

    yield "[DONE]"


@app.post("/api/campaign/run")
async def run_campaign(request: CampaignRequest):
    """Stream campaign generation events via SSE."""
    return EventSourceResponse(orchestrate_campaign(request))


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "llm_provider": "Groq (FREE)",
        "model": GROQ_MODEL,
        "agents": ["Research", "Sentiment", "Content", "Critic"],
    }
