from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class AgentName(str, Enum):
    RESEARCH = "Research Agent"
    SENTIMENT = "Sentiment Agent"
    CONTENT = "Content Agent"
    CRITIC = "Critic Agent"
    ORCHESTRATOR = "Orchestrator"


class CampaignRequest(BaseModel):
    topic: str
    target_audience: str
    tone: str = "Professional"
    campaign_goal: str = "Brand Awareness"


class ResearchBrief(BaseModel):
    topic: str
    key_facts: List[str]
    market_context: str
    competitors: List[str]
    opportunities: List[str]


class SentimentReport(BaseModel):
    overall_sentiment: str
    pain_points: List[str]
    emotional_triggers: List[str]
    trend_score: float  # 0-10
    recommended_angle: str


class CampaignContent(BaseModel):
    tagline: str
    email_subject: str
    email_body: str
    social_posts: List[str]
    call_to_action: str


class CriticReview(BaseModel):
    overall_score: float  # 0-10
    strengths: List[str]
    weaknesses: List[str]
    revision_notes: Optional[str]
    approved: bool


class AgentEvent(BaseModel):
    agent: AgentName
    status: str  # "thinking" | "done" | "error"
    message: str
    data: Optional[dict] = None


class CampaignResult(BaseModel):
    request: CampaignRequest
    research: ResearchBrief
    sentiment: SentimentReport
    content: CampaignContent
    review: CriticReview
    revised_content: Optional[CampaignContent] = None
    total_iterations: int = 1
