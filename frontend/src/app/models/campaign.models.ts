export interface CampaignRequest {
  topic: string;
  target_audience: string;
  tone: string;
  campaign_goal: string;
}

export interface ResearchBrief {
  topic: string;
  key_facts: string[];
  market_context: string;
  competitors: string[];
  opportunities: string[];
}

export interface SentimentReport {
  overall_sentiment: string;
  pain_points: string[];
  emotional_triggers: string[];
  trend_score: number;
  recommended_angle: string;
}

export interface CampaignContent {
  tagline: string;
  email_subject: string;
  email_body: string;
  social_posts: string[];
  call_to_action: string;
}

export interface CriticReview {
  overall_score: number;
  strengths: string[];
  weaknesses: string[];
  revision_notes: string | null;
  approved: boolean;
}

export interface AgentEvent {
  agent: string;
  status: 'thinking' | 'done' | 'error';
  message: string;
  data?: any;
}

export interface CampaignResult {
  request: CampaignRequest;
  research: ResearchBrief;
  sentiment: SentimentReport;
  content: CampaignContent;
  original_content: CampaignContent | null;
  review: CriticReview;
  total_iterations: number;
}

// SVG icon paths (Heroicons MIT) — rendered via [innerHTML] in templates
export const AGENT_ICONS: Record<string, string> = {
  'Research Agent': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
  'Sentiment Agent': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><polyline points="8 21 12 17 16 21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
  'Content Agent': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
  'Critic Agent': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
  'Orchestrator': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
};

export const TONE_OPTIONS = ['Inspiring', 'Professional', 'Playful', 'Urgent', 'Empathetic'];
export const GOAL_OPTIONS = [
  'Brand Awareness',
  'Lead Generation',
  'Product Launch',
  'Customer Retention',
  'Event Promotion',
];
