"""Sales / checkout routes — thin. All protected."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.deps import (
    checkout_use_case,
    current_user,
    get_sale_use_case,
    list_sales_use_case,
)
from app.application.errors import (
    EmptyCart,
    InsufficientStock,
    ProductInactive,
    ProductNotFound,
)
from app.application.use_cases.checkout import CartLine, Checkout, CheckoutCommand
from app.application.use_cases.sales_history import GetSale, ListRecentSales, SaleNotFound
from app.domain.entities.user import User
from app.schemas.sale import CheckoutRequest, SaleResponse

router = APIRouter(prefix="/sales", tags=["sales"], dependencies=[Depends(current_user)])


@router.post(
    "", response_model=SaleResponse, status_code=status.HTTP_201_CREATED,
    summary="Complete a sale (checkout)",
)
def checkout(
    body: CheckoutRequest,
    user: User = Depends(current_user),
    use_case: Checkout = Depends(checkout_use_case),
) -> SaleResponse:
    command = CheckoutCommand(
        lines=tuple(CartLine(product_id=l.product_id, quantity=l.quantity) for l in body.lines),
        payment_method=body.payment_method,
    )
    try:
        sale = use_case.execute(command, cashier_id=user.id)
    except EmptyCart as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Cart is empty") from exc
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "A product was not found") from exc
    except ProductInactive as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Product is no longer available: {exc}"
        ) from exc
    except InsufficientStock as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Not enough stock for: {exc}"
        ) from exc
    return SaleResponse.from_entity(sale)


@router.get("", response_model=list[SaleResponse], summary="Recent sales")
def list_sales(
    limit: int = Query(default=50, ge=1, le=200),
    use_case: ListRecentSales = Depends(list_sales_use_case),
) -> list[SaleResponse]:
    return [SaleResponse.from_entity(s) for s in use_case.execute(limit=limit)]


@router.get("/{sale_id}", response_model=SaleResponse, summary="Get a sale (receipt)")
def get_sale(
    sale_id: UUID,
    use_case: GetSale = Depends(get_sale_use_case),
) -> SaleResponse:
    try:
        return SaleResponse.from_entity(use_case.execute(sale_id))
    except SaleNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sale not found") from exc
