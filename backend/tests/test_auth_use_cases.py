"""Unit tests for auth use-cases using in-memory fakes — no DB, no framework.

Demonstrates that the business logic is fully testable through the ports (DIP + ISP).
"""

import uuid

import pytest

from app.application.errors import EmailAlreadyRegistered, InvalidCredentials
from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.register_user import RegisterUser, RegisterUserCommand
from app.domain.entities.user import User, UserRole


class FakeUserRepository:
    def __init__(self) -> None:
        self._by_email: dict[str, tuple[User, str]] = {}

    def get_by_email(self, email: str) -> User | None:
        row = self._by_email.get(email)
        return row[0] if row else None

    def get_password_hash(self, email: str) -> str | None:
        row = self._by_email.get(email)
        return row[1] if row else None

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        for user, _ in self._by_email.values():
            if user.id == user_id:
                return user
        return None

    def create(self, *, email, full_name, role, password_hash) -> User:
        user = User(id=uuid.uuid4(), email=email, full_name=full_name, role=role)
        self._by_email[email] = (user, password_hash)
        return user


class FakeHasher:
    def hash(self, plain: str) -> str:
        return f"hashed::{plain}"

    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed::{plain}"


class FakeTokenService:
    def issue_access_token(self, *, subject: uuid.UUID) -> str:
        return f"token::{subject}"

    def read_subject(self, token: str) -> uuid.UUID | None:
        try:
            return uuid.UUID(token.removeprefix("token::"))
        except ValueError:
            return None


def _cmd(**kw):
    base = dict(email="a@b.com", full_name="A B", password="secret123")
    base.update(kw)
    return RegisterUserCommand(**base)


def test_register_creates_user_and_normalizes_email() -> None:
    repo = FakeUserRepository()
    RegisterUser(repo, FakeHasher()).execute(_cmd(email="  Owner@Store.COM "))
    assert repo.get_by_email("owner@store.com") is not None


def test_register_rejects_duplicate_email() -> None:
    repo = FakeUserRepository()
    uc = RegisterUser(repo, FakeHasher())
    uc.execute(_cmd())
    with pytest.raises(EmailAlreadyRegistered):
        uc.execute(_cmd())


def test_authenticate_returns_token_on_valid_credentials() -> None:
    repo = FakeUserRepository()
    RegisterUser(repo, FakeHasher()).execute(_cmd())
    result = AuthenticateUser(repo, FakeHasher(), FakeTokenService()).execute(
        email="a@b.com", password="secret123"
    )
    assert result.access_token.startswith("token::")
    assert result.user.role == UserRole.OWNER


def test_authenticate_rejects_wrong_password() -> None:
    repo = FakeUserRepository()
    RegisterUser(repo, FakeHasher()).execute(_cmd())
    with pytest.raises(InvalidCredentials):
        AuthenticateUser(repo, FakeHasher(), FakeTokenService()).execute(
            email="a@b.com", password="nope"
        )


def test_authenticate_rejects_unknown_email() -> None:
    with pytest.raises(InvalidCredentials):
        AuthenticateUser(FakeUserRepository(), FakeHasher(), FakeTokenService()).execute(
            email="ghost@b.com", password="secret123"
        )
