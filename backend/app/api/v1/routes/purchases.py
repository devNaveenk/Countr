"""Purchases / receive-stock routes — thin. All protected."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.deps import (
    current_user,
    get_purchase_use_case,
    list_purchases_use_case,
    receive_stock_use_case,
)
from app.application.errors import EmptyPurchase, ProductNotFound
from app.application.use_cases.purchase_history import (
    GetPurchase,
    ListRecentPurchases,
    PurchaseNotFound,
)
from app.application.use_cases.receive_stock import (
    ReceiveLine,
    ReceiveStock,
    ReceiveStockCommand,
)
from app.domain.entities.user import User
from app.schemas.purchase import PurchaseResponse, ReceiveStockRequest

router = APIRouter(prefix="/purchases", tags=["purchases"], dependencies=[Depends(current_user)])


@router.post(
    "", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED,
    summary="Receive stock (record a purchase)",
)
def receive_stock(
    body: ReceiveStockRequest,
    user: User = Depends(current_user),
    use_case: ReceiveStock = Depends(receive_stock_use_case),
) -> PurchaseResponse:
    command = ReceiveStockCommand(
        lines=tuple(
            ReceiveLine(product_id=l.product_id, quantity=l.quantity, unit_cost=l.unit_cost)
            for l in body.lines
        ),
        supplier_name=body.supplier_name,
        note=body.note,
    )
    try:
        purchase = use_case.execute(command, received_by=user.id)
    except EmptyPurchase as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Nothing to receive"
        ) from exc
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "A product was not found") from exc
    return PurchaseResponse.from_entity(purchase)


@router.get("", response_model=list[PurchaseResponse], summary="Recent purchases")
def list_purchases(
    limit: int = Query(default=50, ge=1, le=200),
    use_case: ListRecentPurchases = Depends(list_purchases_use_case),
) -> list[PurchaseResponse]:
    return [PurchaseResponse.from_entity(p) for p in use_case.execute(limit=limit)]


@router.get("/{purchase_id}", response_model=PurchaseResponse, summary="Get a purchase")
def get_purchase(
    purchase_id: UUID,
    use_case: GetPurchase = Depends(get_purchase_use_case),
) -> PurchaseResponse:
    try:
        return PurchaseResponse.from_entity(use_case.execute(purchase_id))
    except PurchaseNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Purchase not found") from exc
