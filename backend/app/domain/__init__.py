"""Domain layer — the pure business core.

MUST NOT import from `api`, `application`, or `infrastructure`, and must not import
web/DB frameworks. It defines entities and abstract repository interfaces (ports).
Concrete implementations live in `infrastructure` and are injected in (DIP).
"""
