import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { timeout } from 'rxjs';
import { ApiService, Dataset, Model } from './api.service';

@Component({ selector: 'app-prediction', imports: [CommonModule, FormsModule], templateUrl: './prediction.html' })
export class PredictionComponent implements OnInit {
  private api = inject(ApiService);
  private changeDetector = inject(ChangeDetectorRef);
  datasets: Dataset[] = []; models: Model[] = []; datasetId = ''; modelId = '';
  values: Record<string, number | null> = {}; result = ''; error = ''; loading = false;
  get dataset() { return this.datasets.find(item => item.id === this.datasetId); }
  get availableModels() { return this.models.filter(item => item.dataset_id === this.datasetId); }
  get model() { return this.availableModels.find(item => item.id === this.modelId); }
  ngOnInit() {
    this.api.datasets().subscribe({
      next: data => { this.datasets = data; this.changeDetector.markForCheck(); },
      error: () => { this.error = 'Could not load datasets. Check that the API is running.'; this.changeDetector.markForCheck(); }
    });
    this.api.models().subscribe({
      next: data => { this.models = data; this.changeDetector.markForCheck(); },
      error: () => { this.error = 'Could not load models. Check that the API is running.'; this.changeDetector.markForCheck(); }
    });
  }
  datasetChanged() { this.values = {}; this.modelId = ''; this.result = ''; }
  modelChanged() { this.result = ''; }
  submit() {
    if (!this.dataset || !this.model || this.dataset.features.some(f => typeof this.values[f.id] !== 'number' || !Number.isFinite(this.values[f.id]) || this.values[f.id]! <= 0)) { this.error = 'Enter a positive number for every measurement and select a model.'; return; }
    this.error = ''; this.result = ''; this.loading = true;
    this.api.predict(this.datasetId, this.modelId, this.values as Record<string, number>).pipe(timeout(30000)).subscribe({
      next: response => { this.result = response.species; this.loading = false; this.changeDetector.markForCheck(); },
      error: () => { this.error = 'Prediction failed or timed out. Please check the API and try again.'; this.loading = false; this.changeDetector.markForCheck(); }
    });
  }
}
