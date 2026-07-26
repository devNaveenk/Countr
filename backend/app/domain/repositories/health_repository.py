"""A tiny port used to demonstrate the layering end-to-end.

`HealthRepository` is an abstraction (Interface Segregation: it exposes only what the
health use-case needs). The application layer depends on THIS, never on a concrete DB
class — that is Dependency Inversion. A real implementation lives in
`infrastructure/repositories/`, and tests can supply a fake.

This is intentionally trivial so it does not lock in any business data model; the real
domain entities (products, sales, stock, ...) arrive with Phase 1.
"""

from typing import Protocol


class HealthRepository(Protocol):
    def check_database(self) -> bool:
        """Return True if the datastore is reachable and responsive."""
        ...
