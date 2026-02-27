"""
Critic Agent — Reviews campaign content and scores it against a rubric.
This is the quality gate. If score < 7.0, it requests a revision from the Content Agent.
This creates the feedback loop that makes the system truly multi-agent.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import CriticReview, CampaignContent, CampaignRequest, SentimentReport
import json

REVISION_THRESHOLD = 7.0

SYSTEM_PROMPT = """You are a ruthlessly honest Creative Director and Marketing Strategist.
Your job is to review campaign content and provide a fair, rigorous assessment.

Evaluate content on these criteria:
1. Tone alignment (does it match the requested tone?)
2. Audience resonance (does it speak to the audience's pain points and triggers?)
3. Clarity and impact (is the message clear and compelling?)
4. Originality (is it fresh, or generic?)
5. Call to action strength (is the CTA clear and motivating?)

You MUST respond with valid JSON matching this schema:
{
  "overall_score": 7.5,
  "strengths": ["list of 2-4 genuine strengths"],
  "weaknesses": ["list of 2-3 specific weaknesses"],
  "revision_notes": "Specific, actionable revision instructions OR null if approved",
  "approved": true
}

overall_score is 0-10. Set approved=true if score >= 7.0.
If score < 7.0, set approved=false and provide specific revision_notes.
Be constructive but honest. Vague feedback is useless."""


async def run_critic_agent(
    request: CampaignRequest,
    content: CampaignContent,
    sentiment: SentimentReport,
    llm: ChatGroq,
    iteration: int = 1,
) -> CriticReview:
    """Execute the Critic Agent to review and score the campaign content."""

    human_prompt = f"""
Campaign Parameters:
- Topic: {request.topic}
- Target Audience: {request.target_audience}
- Required Tone: {request.tone}
- Goal: {request.campaign_goal}

Audience Context:
- Pain points: {', '.join(sentiment.pain_points[:3])}
- Emotional triggers: {', '.join(sentiment.emotional_triggers[:3])}

Content to Review (Iteration #{iteration}):
TAGLINE: {content.tagline}
EMAIL SUBJECT: {content.email_subject}
EMAIL BODY:
{content.email_body}

SOCIAL POSTS:
- Instagram: {content.social_posts[0] if content.social_posts else 'N/A'}
- Twitter/X: {content.social_posts[1] if len(content.social_posts) > 1 else 'N/A'}
- LinkedIn: {content.social_posts[2] if len(content.social_posts) > 2 else 'N/A'}

CTA: {content.call_to_action}

Review this content rigorously. Return only valid JSON.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ]

    response = await llm.ainvoke(messages)
    raw = response.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)

    # Enforce threshold logic regardless of what LLM decided
    score = data.get("overall_score", 0)
    data["approved"] = score >= REVISION_THRESHOLD

    if not data["approved"] and not data.get("revision_notes"):
        data["revision_notes"] = "Please improve the content based on the weaknesses noted."

    if data["approved"]:
        data["revision_notes"] = None

    return CriticReview(**data)
