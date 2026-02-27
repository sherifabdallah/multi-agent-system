import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CampaignRequest, TONE_OPTIONS, GOAL_OPTIONS } from '../../models/campaign.models';

@Component({
  selector: 'app-campaign-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './campaign-form.component.html',
  styleUrls: ['./campaign-form.component.css']
})
export class CampaignFormComponent {
  @Input() running = false;
  @Output() submitted = new EventEmitter<CampaignRequest>();

  tones = TONE_OPTIONS;
  goals = GOAL_OPTIONS;

  request: CampaignRequest = {
    topic: 'Sustainable Coffee Pods',
    target_audience: 'Eco-conscious millennials',
    tone: 'Inspiring',
    campaign_goal: 'Brand Awareness',
  };

  submit() {
    if (!this.request.topic || !this.request.target_audience) return;
    this.submitted.emit({ ...this.request });
  }
}
