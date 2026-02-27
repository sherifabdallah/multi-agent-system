import { Component, Input, AfterViewChecked, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgentEvent, AGENT_ICONS } from '../../models/campaign.models';

@Component({
  selector: 'app-agent-feed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './agent-feed.component.html',
  styleUrls: ['./agent-feed.component.css']
})
export class AgentFeedComponent implements AfterViewChecked {
  @Input() events: AgentEvent[] = [];
  @ViewChild('feedEnd') feedEnd!: ElementRef;

  getIcon(agent: string): string {
    return AGENT_ICONS[agent] || `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="2" x2="9" y2="4"/><line x1="15" y1="2" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="22"/><line x1="15" y1="20" x2="15" y2="22"/><line x1="2" y1="9" x2="4" y2="9"/><line x1="2" y1="15" x2="4" y2="15"/><line x1="20" y1="9" x2="22" y2="9"/><line x1="20" y1="15" x2="22" y2="15"/></svg>`;
  }

  trackByIndex(index: number): number {
    return index;
  }

  ngAfterViewChecked() {
    if (this.feedEnd) {
      this.feedEnd.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
}
