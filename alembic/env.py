"""
For automatic models import
"""
import importlib
import pkgutil
from pathlib import Path

"""
To get synchronous database connection URL
"""
from config import config as app_config

"""
Register metadata using advanced alchemy
"""
from advanced_alchemy.base import orm_registry

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

DATABASE_URL = app_config.db.url(is_async=False)
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = orm_registry.metadata


def import_all_models():
    """
    For automatic models import
    """
    app_dir = Path(__file__).parent.parent / "src"

    for module_info in pkgutil.iter_modules([str(app_dir)]):
        models_module = f"src.{module_info.name}.models"
        try:
            importlib.import_module(models_module)
        except ModuleNotFoundError:
            continue


import_all_models()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
