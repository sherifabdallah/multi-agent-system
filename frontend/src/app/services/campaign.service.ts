import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { AgentEvent, CampaignRequest } from '../models/campaign.models';

@Injectable({ providedIn: 'root' })
export class CampaignService {
  private readonly API_BASE = 'http://localhost:8000';

  runCampaign(request: CampaignRequest): Observable<AgentEvent> {
    const subject = new Subject<AgentEvent>();

    fetch(`${this.API_BASE}/api/campaign/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    }).then(response => {
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      const read = () => {
        reader.read().then(({ done, value }) => {
          if (done) {
            subject.complete();
            return;
          }

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() ?? '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6).trim();
              if (data === '[DONE]') {
                subject.complete();
                return;
              }
              if (data) {
                try {
                  const event: AgentEvent = JSON.parse(data);
                  subject.next(event);
                } catch (e) {
                    console.warn('[SSE] Failed to parse event data:', data, e);
                }
              }
            }
          }
          read();
        }).catch(err => subject.error(err));
      };

      read();
    }).catch(err => subject.error(err));

    return subject.asObservable();
  }
}
