"""RegisterUser use-case.

Depends only on abstractions: UserRepository + PasswordHasher (DIP). It enforces the one
business rule that belongs here — an email can register only once — and delegates
persistence and hashing to injected ports.
"""

from dataclasses import dataclass

from app.application.errors import EmailAlreadyRegistered
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.domain.security import PasswordHasher


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    full_name: str
    password: str
    role: UserRole = UserRole.OWNER


class RegisterUser:
    def __init__(self, users: UserRepository, hasher: PasswordHasher) -> None:
        self._users = users
        self._hasher = hasher

    def execute(self, cmd: RegisterUserCommand) -> User:
        email = cmd.email.strip().lower()
        if self._users.get_by_email(email) is not None:
            raise EmailAlreadyRegistered(email)
        return self._users.create(
            email=email,
            full_name=cmd.full_name.strip(),
            role=cmd.role,
            password_hash=self._hasher.hash(cmd.password),
        )
