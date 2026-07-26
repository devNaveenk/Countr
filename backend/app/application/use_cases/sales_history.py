"""Read-side use-cases for sales."""

from uuid import UUID

from app.application.errors import ApplicationError
from app.domain.entities.sale import Sale
from app.domain.repositories.sale_repository import SaleRepository


class SaleNotFound(ApplicationError):
    pass


class ListRecentSales:
    def __init__(self, sales: SaleRepository) -> None:
        self._sales = sales

    def execute(self, *, limit: int = 50) -> list[Sale]:
        return self._sales.list_recent(limit=limit)


class GetSale:
    def __init__(self, sales: SaleRepository) -> None:
        self._sales = sales

    def execute(self, sale_id: UUID) -> Sale:
        sale = self._sales.get(sale_id)
        if sale is None:
            raise SaleNotFound(str(sale_id))
        return sale
