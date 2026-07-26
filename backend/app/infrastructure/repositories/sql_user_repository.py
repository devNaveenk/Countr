"""Concrete UserRepository over SQLAlchemy. Maps ORM rows <-> domain entities."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user import UserModel


def _to_entity(row: UserModel) -> User:
    return User(
        id=row.id,
        email=row.email,
        full_name=row.full_name,
        role=UserRole(row.role),
    )


class SqlUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> User | None:
        row = self._session.scalar(select(UserModel).where(UserModel.email == email))
        return _to_entity(row) if row else None

    def get_password_hash(self, email: str) -> str | None:
        return self._session.scalar(
            select(UserModel.password_hash).where(UserModel.email == email)
        )

    def get_by_id(self, user_id: UUID) -> User | None:
        row = self._session.get(UserModel, user_id)
        return _to_entity(row) if row else None

    def create(
        self, *, email: str, full_name: str, role: UserRole, password_hash: str
    ) -> User:
        row = UserModel(
            email=email, full_name=full_name, role=role.value, password_hash=password_hash
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return _to_entity(row)
