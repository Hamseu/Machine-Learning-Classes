import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Run } from './api.service';
@Component({ selector: 'app-runs', imports: [CommonModule], templateUrl: './runs.html' })
export class RunsComponent implements OnInit {
  private api = inject(ApiService);
  private changeDetector = inject(ChangeDetectorRef);
  runs: Run[] = []; error = '';
  ngOnInit() {
    this.api.runs().subscribe({
      next: data => { this.runs = data; this.changeDetector.markForCheck(); },
      error: () => { this.error = 'Could not load MLflow runs.'; this.changeDetector.markForCheck(); }
    });
  }
}
