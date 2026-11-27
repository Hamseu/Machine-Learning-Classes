import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { App } from './app';
import { PredictionComponent } from './prediction';
import { routes } from './app.routes';

describe('Iris workspace', () => {
  beforeEach(() => TestBed.configureTestingModule({ imports: [App, PredictionComponent], providers: [provideRouter(routes), provideHttpClient()] }));
  it('renders navigation to both pages', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Prediction');
    expect(fixture.nativeElement.textContent).toContain('Experiments');
    expect(routes.map(route => route.path)).toEqual(['', 'runs']);
  });
  it('clears values when the dataset changes but keeps them when the model changes', () => {
    const component = TestBed.createComponent(PredictionComponent).componentInstance;
    component.values = { sepal_length: 5.1 };
    component.modelChanged();
    expect(component.values['sepal_length']).toBe(5.1);
    component.datasetChanged();
    expect(component.values).toEqual({});
  });
});
