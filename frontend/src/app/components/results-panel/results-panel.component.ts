import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CampaignResult, AgentEvent, AGENT_ICONS } from '../../models/campaign.models';

@Component({
  selector: 'app-results-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results-panel.component.html',
  styleUrls: ['./results-panel.component.css']
})
export class ResultsPanelComponent {
  @Input() result: CampaignResult | null = null;
  @Input() running = false;
  @Input() events: AgentEvent[] = [];

  platforms = ['Instagram', 'Twitter/X', 'LinkedIn'];
  allAgents = ['Research Agent', 'Sentiment Agent', 'Content Agent', 'Critic Agent'];

  getIcon(agent: string): string {
    return AGENT_ICONS[agent] || `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>`;
  }

  getAgentStatus(agent: string): 'status-done' | 'status-thinking' | 'status-idle' {
    const done = this.events.some(e => e.status === 'done' && e.agent === agent);
    const thinking = this.events.some(e => e.status === 'thinking' && e.agent === agent);
    if (done) return 'status-done';
    if (thinking) return 'status-thinking';
    return 'status-idle';
  }

  get currentAgentMessage(): string {
    const last = [...this.events].reverse().find(e => e.status === 'thinking');
    return last ? `${last.agent} is working...` : 'Initializing...';
  }

  get scoreClass(): string {
    if (!this.result) return '';
    const s = this.result.review.overall_score;
    return s >= 8 ? 'good' : s >= 6 ? 'ok' : 'bad';
  }

  get scoreBarClass(): string {
    if (!this.result) return '';
    const s = this.result.review.overall_score;
    return s >= 8 ? '' : s >= 6 ? 'medium' : 'low';
  }
}
