import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';

export interface HealthResponse {
  status: string;
  database: string;
}

@Injectable({ providedIn: 'root' })
export class HealthService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api/v1/health';

  readonly health = signal<HealthResponse | null>(null);
  readonly error = signal<string | null>(null);

  checkHealth(): void {
    this.http.get<HealthResponse>(this.apiUrl).subscribe({
      next: (res) => {
        this.health.set(res);
        this.error.set(null);
      },
      error: () => {
        this.health.set(null);
        this.error.set('No se pudo conectar con la API de Kairos');
      },
    });
  }
}