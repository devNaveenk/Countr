"""Product catalog routes — thin. All are protected (require a signed-in user)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.deps import (
    adjust_stock_use_case,
    archive_product_use_case,
    create_product_use_case,
    current_user,
    get_product_use_case,
    list_products_use_case,
    update_product_use_case,
)
from app.application.errors import (
    BarcodeAlreadyExists,
    InvalidStockAdjustment,
    ProductNotFound,
)
from app.application.use_cases.product_catalog import (
    AdjustStock,
    ArchiveProduct,
    CreateProduct,
    GetProduct,
    ListProducts,
    ProductInput,
    UpdateProduct,
)
from app.domain.entities.user import User
from app.schemas.product import (
    ProductCreateRequest,
    ProductResponse,
    ProductWriteRequest,
    StockAdjustmentRequest,
)

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(current_user)])


def _to_input(body: ProductWriteRequest) -> ProductInput:
    return ProductInput(
        name=body.name,
        price=body.price,
        cost_price=body.cost_price,
        barcode=body.barcode,
        category=body.category,
        unit=body.unit,
        tax_exempt=body.tax_exempt,
        reorder_level=body.reorder_level,
    )


@router.get("", response_model=list[ProductResponse], summary="List products")
def list_products(
    search: str | None = Query(default=None),
    active_only: bool = Query(default=True),
    low_stock_only: bool = Query(default=False),
    use_case: ListProducts = Depends(list_products_use_case),
) -> list[ProductResponse]:
    products = use_case.execute(
        search=search, active_only=active_only, low_stock_only=low_stock_only
    )
    return [ProductResponse.from_entity(p) for p in products]


@router.post(
    "", response_model=ProductResponse, status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
def create_product(
    body: ProductCreateRequest,
    use_case: CreateProduct = Depends(create_product_use_case),
) -> ProductResponse:
    try:
        product = use_case.execute(_to_input(body), initial_stock=body.initial_stock)
    except BarcodeAlreadyExists as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this barcode already exists",
        ) from exc
    return ProductResponse.from_entity(product)


@router.get("/{product_id}", response_model=ProductResponse, summary="Get a product")
def get_product(
    product_id: UUID,
    use_case: GetProduct = Depends(get_product_use_case),
) -> ProductResponse:
    try:
        return ProductResponse.from_entity(use_case.execute(product_id))
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc


@router.put("/{product_id}", response_model=ProductResponse, summary="Update a product")
def update_product(
    product_id: UUID,
    body: ProductWriteRequest,
    use_case: UpdateProduct = Depends(update_product_use_case),
) -> ProductResponse:
    try:
        return ProductResponse.from_entity(use_case.execute(product_id, _to_input(body)))
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc
    except BarcodeAlreadyExists as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "Barcode already in use") from exc


@router.post(
    "/{product_id}/stock", response_model=ProductResponse, summary="Adjust stock on hand",
)
def adjust_stock(
    product_id: UUID,
    body: StockAdjustmentRequest,
    use_case: AdjustStock = Depends(adjust_stock_use_case),
) -> ProductResponse:
    try:
        return ProductResponse.from_entity(use_case.execute(product_id, delta=body.delta))
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc
    except InvalidStockAdjustment as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Adjustment would make stock negative"
        ) from exc


@router.delete(
    "/{product_id}", response_model=ProductResponse, summary="Archive (soft-delete) a product",
)
def archive_product(
    product_id: UUID,
    _user: User = Depends(current_user),
    use_case: ArchiveProduct = Depends(archive_product_use_case),
) -> ProductResponse:
    try:
        return ProductResponse.from_entity(use_case.execute(product_id))
    except ProductNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc
