"""
Mock external tools — easily swappable for real APIs
(SerpAPI, Google Trends, Brand24, etc.)
"""
from langchain_core.tools import tool
from typing import List
import random


@tool
def search_market_data(topic: str) -> str:
    """Search for market data and competitor information about a topic."""
    # In production: call SerpAPI / Tavily / Brave Search
    return f"""
    Market data for '{topic}':
    - Global market size: $4.2B (2024), projected $6.8B by 2028
    - YoY growth: 14.3%
    - Top competitors: EcoBrews, GreenPod Co., NaturaCup, PureLeaf Industries
    - Key trends: sustainability focus, premium positioning, DTC growth
    - Consumer demand peak: Q4 (holiday gifting)
    """


@tool
def get_audience_insights(audience: str) -> str:
    """Retrieve audience demographic and psychographic insights."""
    # In production: call Facebook Audience Insights API / SparkToro
    return f"""
    Insights for '{audience}':
    - Age range: 25-38 (primary), 18-24 (secondary)
    - Values: environmental impact, quality over price, authenticity
    - Pain points: plastic waste guilt, greenwashing skepticism, premium pricing
    - Preferred channels: Instagram (42%), TikTok (28%), Email (30%)
    - Buying triggers: peer recommendations, certifications, brand transparency
    - Average spend: $45-80/month on premium consumables
    """


@tool
def analyze_content_performance(tone: str, content_type: str) -> str:
    """Analyze historical content performance for a given tone and content type."""
    # In production: call HubSpot / Mailchimp analytics
    scores = {
        "Inspiring": {"email_open_rate": "28%", "ctr": "4.2%", "engagement": "high"},
        "Professional": {"email_open_rate": "22%", "ctr": "3.1%", "engagement": "medium"},
        "Playful": {"email_open_rate": "31%", "ctr": "5.8%", "engagement": "very high"},
        "Urgent": {"email_open_rate": "35%", "ctr": "6.1%", "engagement": "high"},
    }
    data = scores.get(tone, scores["Professional"])
    return f"Performance benchmark for {tone} {content_type}: {data}"


ALL_TOOLS = [search_market_data, get_audience_insights, analyze_content_performance]
