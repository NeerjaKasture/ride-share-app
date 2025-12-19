from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy import String
from sqlmodel import SQLModel
import sqlmodel.sql.sqltypes as sqltypes

from alembic import context

# Import your models here so they are registered with SQLModel
from app.models.rides import Users, Rides, RideUserLink
from app.core.config import settings

# This is the Alembic Config object
config = context.config

# Set the database URL dynamically from settings
config.set_main_option("sqlalchemy.url", settings.POSTGRES_SYNC)

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate support
target_metadata = SQLModel.metadata

# --- FIX: render AutoString as sa.String ---
def render_item(type_, obj, autogen_context):
    if type_ == "type" and isinstance(obj, sqltypes.AutoString):
        return "sa.String()"
    return False

# ---------------- OFFLINE ----------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,  
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------- ONLINE ----------------
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
            render_item=render_item
        )

        with context.begin_transaction():
            context.run_migrations()


# Run migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
