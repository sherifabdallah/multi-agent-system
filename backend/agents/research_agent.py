"""
Research Agent — Gathers market intelligence and topic context.
Uses tools to search for real data, then synthesizes a structured brief.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from models.schemas import ResearchBrief, CampaignRequest
import json


SYSTEM_PROMPT = """You are a Senior Market Research Analyst specializing in marketing intelligence.
Your job is to gather and synthesize relevant information about a product/topic to inform a marketing campaign.

Given the topic, target audience, and campaign goal, produce a structured research brief.

You MUST respond with valid JSON matching this schema:
{
  "topic": "string",
  "key_facts": ["list of 4-6 important facts"],
  "market_context": "2-3 sentence market overview",
  "competitors": ["list of 3-4 competitor names"],
  "opportunities": ["list of 3-4 market opportunities"]
}

Be specific, data-driven, and insightful. No fluff."""


async def run_research_agent(
    request: CampaignRequest,
    llm: ChatGroq,
    market_data: str,
    audience_data: str,
) -> ResearchBrief:
    """Execute the Research Agent to produce a market brief."""

    human_prompt = f"""
Campaign Brief:
- Topic/Product: {request.topic}
- Target Audience: {request.target_audience}
- Campaign Goal: {request.campaign_goal}
- Tone: {request.tone}

Market Research Data:
{market_data}

Audience Insights:
{audience_data}

Synthesize this into a structured research brief. Return only valid JSON.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ]

    response = await llm.ainvoke(messages)
    content = response.content.strip()

    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    data = json.loads(content)
    return ResearchBrief(**data)
