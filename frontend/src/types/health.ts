/** Mirrors the backend HealthResponse DTO (app/schemas/health.py). */
export interface HealthResponse {
  status: "ok" | "degraded";
  api: boolean;
  database: boolean;
  app: string;
  version: string;
}
