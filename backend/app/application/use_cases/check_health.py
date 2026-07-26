"""CheckHealth use-case — demonstrates the full layered flow.

Note the constructor takes the `HealthRepository` *interface*, not a concrete class.
The wiring (which implementation) happens at the edge (api/deps.py). This use-case is
fully unit-testable with a fake repository — no database required.
"""

from dataclasses import dataclass

from app.domain.repositories.health_repository import HealthRepository


@dataclass(frozen=True)
class HealthResult:
    api_ok: bool
    database_ok: bool

    @property
    def healthy(self) -> bool:
        return self.api_ok and self.database_ok


class CheckHealth:
    def __init__(self, health_repository: HealthRepository) -> None:
        self._repo = health_repository

    def execute(self) -> HealthResult:
        return HealthResult(api_ok=True, database_ok=self._repo.check_database())
