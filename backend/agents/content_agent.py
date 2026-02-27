"""
Content Agent — Generates campaign copy based on research and sentiment context.
Produces a complete campaign package: tagline, email, social posts, CTA.
Can accept revision notes from the Critic for a second pass.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import CampaignContent, ResearchBrief, SentimentReport, CampaignRequest
from typing import Optional
import json
import re


SYSTEM_PROMPT = """You are an award-winning Marketing Copywriter with expertise in brand storytelling.
You craft compelling, human-centered campaign content that converts.

Given research, sentiment analysis, and campaign parameters, produce a complete campaign package.

You MUST respond with valid JSON matching this schema:
{
  "tagline": "Punchy 5-10 word brand tagline",
  "email_subject": "Email subject line (max 60 chars)",
  "email_body": "Full email body (150-250 words, with clear structure)",
  "social_posts": ["Instagram post", "Twitter/X post", "LinkedIn post"],
  "call_to_action": "Clear, action-oriented CTA button text"
}

Guidelines:
- Match the specified tone precisely
- Speak directly to the audience's pain points and emotional triggers
- Be specific, not generic
- Make every word count"""


async def run_content_agent(
    request: CampaignRequest,
    research: ResearchBrief,
    sentiment: SentimentReport,
    llm: ChatGroq,
    revision_notes: Optional[str] = None,
) -> CampaignContent:
    """Execute the Content Agent to generate campaign copy."""

    revision_section = ""
    if revision_notes:
        revision_section = f"""
⚠️ REVISION REQUEST from Critic Agent:
{revision_notes}
Please address ALL revision notes in this new version.
"""

    human_prompt = f"""
Campaign Parameters:
- Product/Topic: {request.topic}
- Target Audience: {request.target_audience}
- Tone: {request.tone}
- Goal: {request.campaign_goal}

Research Intelligence:
- Market context: {research.market_context}
- Key facts: {chr(10).join(f'  • {f}' for f in research.key_facts)}
- Opportunities: {chr(10).join(f'  • {o}' for o in research.opportunities)}

Audience Sentiment:
- Overall mood: {sentiment.overall_sentiment}
- Pain points: {chr(10).join(f'  • {p}' for p in sentiment.pain_points)}
- Emotional triggers: {chr(10).join(f'  • {t}' for t in sentiment.emotional_triggers)}
- Strategic angle: {sentiment.recommended_angle}
{revision_section}
Generate the complete campaign content package. Return only valid JSON.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ]

    response = await llm.ainvoke(messages)
    content = response.content.strip()

    # Strip markdown code fences if present
    if "```" in content:
        # Extract content between the first ``` and last ```
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", content)
        if fence_match:
            content = fence_match.group(1).strip()

    # Replace literal (unescaped) control characters inside JSON strings.
    # json.loads rejects raw \n, \r, \t etc. inside string values.
    def _escape_control_chars(s: str) -> str:
        """Escape bare control characters that are invalid inside JSON strings."""
        result = []
        in_string = False
        escape_next = False
        for ch in s:
            if escape_next:
                result.append(ch)
                escape_next = False
                continue
            if ch == "\\":
                escape_next = True
                result.append(ch)
                continue
            if ch == '"':
                in_string = not in_string
                result.append(ch)
                continue
            if in_string and ord(ch) < 0x20:
                # Replace bare control chars with their JSON escape sequences
                replacements = {
                    '\n': '\\n',
                    '\r': '\\r',
                    '\t': '\\t',
                    '\b': '\\b',
                    '\f': '\\f',
                }
                result.append(replacements.get(ch, f'\\u{ord(ch):04x}'))
            else:
                result.append(ch)
        return ''.join(result)

    content = _escape_control_chars(content)
    data = json.loads(content)
    return CampaignContent(**data)
