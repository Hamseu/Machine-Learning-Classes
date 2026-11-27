import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Feature { id: string; label: string; unit: string; }
export interface Dataset { id: string; name: string; description: string; features: Feature[]; }
export interface Model { id: string; name: string; dataset_id: string; metrics: Record<string, number>; params: Record<string, string>; }
export interface Run { id: string; name: string; status: string; started_at: number; metrics: Record<string, number>; params: Record<string, string>; tags: Record<string, string>; }
@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  datasets() { return this.http.get<Dataset[]>('/api/datasets'); }
  models() { return this.http.get<Model[]>('/api/models'); }
  runs() { return this.http.get<Run[]>('/api/runs'); }
  predict(dataset_id: string, model_id: string, features: Record<string, number>) {
    return this.http.post<{species: string}>('/api/predict', { dataset_id, model_id, features });
  }
}
