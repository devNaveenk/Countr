"""Application-level errors — framework-agnostic.

The API layer maps these to HTTP status codes; the domain/application never imports HTTP.
"""


class ApplicationError(Exception):
    """Base class for expected, handled application errors."""


class EmailAlreadyRegistered(ApplicationError):
    pass


class InvalidCredentials(ApplicationError):
    pass
