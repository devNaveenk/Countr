"""Unit test for the CheckHealth use-case using a fake repository.

No FastAPI, no database. This is the payoff of Dependency Inversion: the use-case is
tested in isolation by substituting the port (Liskov).
"""

from app.application.use_cases.check_health import CheckHealth
from app.domain.repositories.health_repository import HealthRepository


class FakeHealthRepository(HealthRepository):
    def __init__(self, db_ok: bool) -> None:
        self._db_ok = db_ok

    def check_database(self) -> bool:
        return self._db_ok


def test_healthy_when_database_ok() -> None:
    result = CheckHealth(FakeHealthRepository(db_ok=True)).execute()
    assert result.api_ok is True
    assert result.database_ok is True
    assert result.healthy is True


def test_degraded_when_database_down() -> None:
    result = CheckHealth(FakeHealthRepository(db_ok=False)).execute()
    assert result.database_ok is False
    assert result.healthy is False
