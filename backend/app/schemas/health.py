"""Boundary DTOs (Pydantic). Domain objects never go on the wire directly."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str          # "ok" | "degraded"
    api: bool
    database: bool
    app: str
    version: str
