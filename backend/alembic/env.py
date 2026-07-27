"""Alembic environment — wired to Countr's settings and ORM metadata.

URL comes from app settings (single source of truth). target_metadata is our declarative
Base with all models imported, so `alembic revision --autogenerate` sees every table.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_settings
from app.infrastructure.db.session import Base

# Import all ORM models here so autogenerate can detect them.
from app.infrastructure.db.models.product import ProductModel  # noqa: F401
from app.infrastructure.db.models.purchase import (  # noqa: F401
    PurchaseItemModel,
    PurchaseModel,
)
from app.infrastructure.db.models.sale import SaleItemModel, SaleModel  # noqa: F401
from app.infrastructure.db.models.stock_movement import (  # noqa: F401
    StockMovementModel,
)
from app.infrastructure.db.models.user import UserModel  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
