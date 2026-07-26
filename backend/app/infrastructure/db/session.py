"""SQLAlchemy engine, session factory, and the ORM declarative base.

The engine is created lazily from settings so importing this module never forces a DB
connection (keeps tests and app startup fast). ORM models (Phase 1) inherit `Base`.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models (infrastructure/db/models/)."""


_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _init() -> None:
    global _engine, _SessionLocal
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)


def get_engine() -> Engine:
    _init()
    assert _engine is not None
    return _engine


def get_session() -> Iterator[Session]:
    """Yield a session and always close it. Used as a FastAPI dependency."""
    _init()
    assert _SessionLocal is not None
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()
