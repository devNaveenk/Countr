"""Reports route — a store overview over a rolling time window. Protected."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import current_user, store_report_use_case
from app.application.use_cases.store_report import GetStoreReport
from app.schemas.report import StoreReportResponse

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(current_user)])


@router.get("/overview", response_model=StoreReportResponse, summary="Store overview report")
def overview(
    days: int = Query(default=7, ge=1, le=365, description="Rolling window in days"),
    use_case: GetStoreReport = Depends(store_report_use_case),
) -> StoreReportResponse:
    since = datetime.now(UTC) - timedelta(days=days)
    report = use_case.execute(since=since)
    return StoreReportResponse.from_report(report, period_days=days)
