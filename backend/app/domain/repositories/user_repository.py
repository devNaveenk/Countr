"""UserRepository port — the abstraction the auth use-cases depend on (DIP).

Segregated to just what auth needs (ISP). The returned/consumed objects include the
password hash only where necessary; the hash never leaves the backend.
"""

from typing import Protocol
from uuid import UUID

from app.domain.entities.user import User, UserRole


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> User | None: ...

    def get_password_hash(self, email: str) -> str | None:
        """Return the stored password hash for the email, or None if no such user."""
        ...

    def create(
        self, *, email: str, full_name: str, role: UserRole, password_hash: str
    ) -> User: ...

    def get_by_id(self, user_id: UUID) -> User | None: ...
