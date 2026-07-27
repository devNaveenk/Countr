"""User entity — a plain business object (no ORM, no framework).

Holds identity + role. Passwords are never stored here in plain text; the hash lives on
the persistence model. Roles are intentionally minimal for Phase 1 (owner runs the store,
cashier operates the till).
"""

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class UserRole(StrEnum):
    OWNER = "owner"
    CASHIER = "cashier"


@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    full_name: str
    role: UserRole
