"""Composition root for v1 — where abstractions are bound to implementations.

This is the ONE place allowed to know both the domain ports and their concrete
infrastructure implementations. Routes ask for a use-case; they never construct
repositories or sessions themselves.
"""

from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.check_health import CheckHealth
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.sql_health_repository import SqlHealthRepository


def db_session() -> Iterator[Session]:
    yield from get_session()


def check_health_use_case(session: Session = Depends(db_session)) -> CheckHealth:
    repository = SqlHealthRepository(session)
    return CheckHealth(repository)
