"""Application-level errors — framework-agnostic.

The API layer maps these to HTTP status codes; the domain/application never imports HTTP.
"""


class ApplicationError(Exception):
    """Base class for expected, handled application errors."""


class EmailAlreadyRegistered(ApplicationError):
    pass


class InvalidCredentials(ApplicationError):
    pass


class ProductNotFound(ApplicationError):
    pass


class BarcodeAlreadyExists(ApplicationError):
    pass


class InvalidStockAdjustment(ApplicationError):
    """Raised when an adjustment would drive stock negative."""


class EmptyCart(ApplicationError):
    pass


class ProductInactive(ApplicationError):
    pass


class InsufficientStock(ApplicationError):
    pass


class EmptyPurchase(ApplicationError):
    pass
