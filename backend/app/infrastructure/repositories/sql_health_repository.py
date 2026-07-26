"""Concrete `HealthRepository` backed by SQLAlchemy.

Implements the domain port (Liskov: usable anywhere the interface is expected). It
performs a trivial `SELECT 1` to confirm the database answers.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.repositories.health_repository import HealthRepository


class SqlHealthRepository(HealthRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def check_database(self) -> bool:
        try:
            self._session.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False
