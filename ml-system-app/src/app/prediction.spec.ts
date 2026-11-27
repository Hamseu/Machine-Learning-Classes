import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { PredictionComponent } from './prediction';

describe('Prediction rendering', () => {
  it('shows an asynchronous result and stops loading', async () => {
    TestBed.configureTestingModule({ imports: [PredictionComponent], providers: [provideHttpClient(), provideHttpClientTesting()] });
    const fixture = TestBed.createComponent(PredictionComponent);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
    http.expectOne('/api/datasets').flush([{ id: 'iris', name: 'Iris', description: '', features: [{ id: 'length', label: 'Length', unit: 'cm' }] }]);
    http.expectOne('/api/models').flush([{ id: 'model', name: 'Model', dataset_id: 'iris', metrics: {}, params: {} }]);
    await fixture.whenStable();
    const dataset = fixture.nativeElement.querySelector('#dataset') as HTMLSelectElement;
    dataset.value = 'iris'; dataset.dispatchEvent(new Event('change'));
    await fixture.whenStable();
    const model = fixture.nativeElement.querySelector('#model') as HTMLSelectElement;
    model.value = 'model'; model.dispatchEvent(new Event('change'));
    await fixture.whenStable();
    const input = fixture.nativeElement.querySelector('#length') as HTMLInputElement;
    input.value = '5.1'; input.dispatchEvent(new Event('input'));
    await fixture.whenStable();
    fixture.nativeElement.querySelector('form').dispatchEvent(new Event('submit'));
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('Predicting');
    http.expectOne('/api/predict').flush({ species: 'Setosa' });
    await fixture.whenStable();
    expect(fixture.nativeElement.textContent).toContain('Setosa');
    expect(fixture.nativeElement.textContent).not.toContain('Predicting');
    http.verify();
  });
});
