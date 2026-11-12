import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = None

def get_url() -> str:
    url = os.getenv("MIGRATION_DATABASE_URL")
    if not url or "CHANGE_ME" in url:
        raise RuntimeError("MIGRATION_DATABASE_URL을 별도 Migration 연습 DB로 설정하세요.")
    return url

def run_migrations_offline() -> None:
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle":"named"})
    with context.begin_transaction(): context.run_migrations()

def run_migrations_online() -> None:
    engine = create_engine(get_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction(): context.run_migrations()

if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
