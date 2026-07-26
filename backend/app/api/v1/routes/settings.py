"""Store settings the client needs (currently just the tax rate for live totals)."""

from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.v1.deps import current_user
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/settings", tags=["settings"], dependencies=[Depends(current_user)])


class StoreSettingsResponse(BaseModel):
    tax_rate: Decimal
    currency: str = "USD"


@router.get("", response_model=StoreSettingsResponse, summary="Store settings for the client")
def get_store_settings(settings: Settings = Depends(get_settings)) -> StoreSettingsResponse:
    return StoreSettingsResponse(tax_rate=settings.default_tax_rate)
