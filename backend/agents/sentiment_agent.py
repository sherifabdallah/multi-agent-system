"""
Sentiment Agent — Analyzes audience emotional landscape and trends.
Identifies pain points, triggers, and the best emotional angle for the campaign.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import SentimentReport, ResearchBrief, CampaignRequest
import json


SYSTEM_PROMPT = """You are an Audience Psychology & Sentiment Specialist.
Your expertise is understanding the emotional landscape of target audiences to inform marketing strategy.

Given research context and audience data, produce a sentiment analysis report.

You MUST respond with valid JSON matching this schema:
{
  "overall_sentiment": "string (e.g. 'Cautiously Optimistic', 'Frustrated but Hopeful')",
  "pain_points": ["list of 3-5 specific pain points"],
  "emotional_triggers": ["list of 3-4 positive emotional triggers to leverage"],
  "trend_score": 7.5,
  "recommended_angle": "1-2 sentence strategic recommendation for the emotional angle"
}

trend_score is 0-10 where 10 = perfectly aligned with current trends.
Be empathetic, psychologically astute, and strategic."""


async def run_sentiment_agent(
    request: CampaignRequest,
    research: ResearchBrief,
    llm: ChatGroq,
    audience_data: str,
    performance_data: str,
) -> SentimentReport:
    """Execute the Sentiment Agent to produce an audience analysis."""

    human_prompt = f"""
Campaign Context:
- Topic: {request.topic}
- Target Audience: {request.target_audience}
- Tone: {request.tone}
- Goal: {request.campaign_goal}

Research Brief Summary:
- Key facts: {', '.join(research.key_facts[:3])}
- Opportunities: {', '.join(research.opportunities)}

Raw Audience Data:
{audience_data}

Content Performance Benchmarks:
{performance_data}

Analyze the audience sentiment and emotional landscape. Return only valid JSON.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ]

    response = await llm.ainvoke(messages)
    content = response.content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    data = json.loads(content)
    return SentimentReport(**data)
