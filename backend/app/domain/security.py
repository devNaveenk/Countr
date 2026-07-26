"""Security ports — abstractions for hashing and tokens.

Kept in the domain so the application layer depends on these interfaces, not on bcrypt or
PyJWT (DIP). Concrete implementations live in `infrastructure/security/` and are swappable
(e.g. change hashing algorithm) without touching use-cases.
"""

from typing import Protocol
from uuid import UUID


class PasswordHasher(Protocol):
    def hash(self, plain: str) -> str: ...
    def verify(self, plain: str, hashed: str) -> bool: ...


class TokenService(Protocol):
    def issue_access_token(self, *, subject: UUID) -> str: ...
    def read_subject(self, token: str) -> UUID | None:
        """Return the subject (user id) if the token is valid, else None."""
        ...
