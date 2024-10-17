from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from models import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_online():
    """
    Выполняет миграции Alembic в "online" режиме.
    Команда для миграций:
    alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
