"""Infrastructure layer — the swappable details.

Concrete implementations of domain ports: database, repositories, and external-service
adapters (payments, sales tax, QuickBooks, storage, notifications). This layer depends
on `domain`; nothing in `domain`/`application` depends back on it.
"""
