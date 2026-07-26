"""Read-side use-cases for purchases."""

from uuid import UUID

from app.application.errors import ApplicationError
from app.domain.entities.purchase import Purchase
from app.domain.repositories.purchase_repository import PurchaseRepository


class PurchaseNotFound(ApplicationError):
    pass


class ListRecentPurchases:
    def __init__(self, purchases: PurchaseRepository) -> None:
        self._purchases = purchases

    def execute(self, *, limit: int = 50) -> list[Purchase]:
        return self._purchases.list_recent(limit=limit)


class GetPurchase:
    def __init__(self, purchases: PurchaseRepository) -> None:
        self._purchases = purchases

    def execute(self, purchase_id: UUID) -> Purchase:
        purchase = self._purchases.get(purchase_id)
        if purchase is None:
            raise PurchaseNotFound(str(purchase_id))
        return purchase
