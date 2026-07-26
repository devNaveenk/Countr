"""Health route — thin. It parses/serializes and delegates to the use-case.

No business logic here. This is the whole point of the presentation layer being thin:
it can change (REST -> GraphQL, versioning, ...) without touching domain/application.
"""

from fastapi import APIRouter, Depends

from app import __version__
from app.api.v1.deps import check_health_use_case
from app.application.use_cases.check_health import CheckHealth
from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Liveness/readiness check")
def health(use_case: CheckHealth = Depends(check_health_use_case)) -> HealthResponse:
    result = use_case.execute()
    settings = get_settings()
    return HealthResponse(
        status="ok" if result.healthy else "degraded",
        api=result.api_ok,
        database=result.database_ok,
        app=settings.app_name,
        version=__version__,
    )
