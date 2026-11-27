import { Routes } from '@angular/router';
import { PredictionComponent } from './prediction';
import { RunsComponent } from './runs';
export const routes: Routes = [{ path: '', component: PredictionComponent }, { path: 'runs', component: RunsComponent }];
