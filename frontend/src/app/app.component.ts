import { Component, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { CampaignService } from './services/campaign.service';
import { CampaignFormComponent } from './components/campaign-form/campaign-form.component';
import { AgentFeedComponent } from './components/agent-feed/agent-feed.component';
import { ResultsPanelComponent } from './components/results-panel/results-panel.component';
import { AgentEvent, CampaignRequest, CampaignResult } from './models/campaign.models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, CampaignFormComponent, AgentFeedComponent, ResultsPanelComponent],
  template: `
    <header class="header">
      <span class="header-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="2" x2="9" y2="4"/><line x1="15" y1="2" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="22"/><line x1="15" y1="20" x2="15" y2="22"/><line x1="2" y1="9" x2="4" y2="9"/><line x1="2" y1="15" x2="4" y2="15"/><line x1="20" y1="9" x2="22" y2="9"/><line x1="20" y1="15" x2="22" y2="15"/></svg>
      </span>
      <h1>Multi-Agent Marketing System</h1>
      <span class="subtitle">4 Specialized AI Agents · Real-time Collaboration</span>
    </header>

    <div class="layout">
      <div class="left-panel">
        <app-campaign-form [running]="running" (submitted)="onSubmit($event)" />
        <app-agent-feed [events]="events" />
      </div>
      <div class="right-panel">
        <app-results-panel [result]="result" [running]="running" [events]="events" />
      </div>
    </div>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnDestroy {
  events: AgentEvent[] = [];
  running = false;
  result: CampaignResult | null = null;
  private sub: Subscription | null = null;

  constructor(private campaignService: CampaignService, private cdr: ChangeDetectorRef) { }

  ngOnDestroy() { this.sub?.unsubscribe(); }

  onSubmit(request: CampaignRequest) {
    this.events = [];
    this.running = true;
    this.result = null;
    this.sub?.unsubscribe();
    this.sub = this.campaignService.runCampaign(request).subscribe({
      next: (ev: AgentEvent) => {
        this.events = [...this.events, ev];
        if (ev.agent === 'Orchestrator' && ev.status === 'done' && ev.data) {
          this.result = ev.data as CampaignResult;
          this.running = false;
        }
        this.cdr.detectChanges();
      },
      error: () => { this.running = false; this.cdr.detectChanges(); },
      complete: () => { this.running = false; this.cdr.detectChanges(); }
    });
  }
}
