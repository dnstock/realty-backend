from logging.config import fileConfig
from typing import Any, List
from sqlalchemy import engine_from_config, pool
from alembic import context
from alembic.operations import ops
from core import settings
from core.utils import clean_multiline_string
from db import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
config.set_main_option("sqlalchemy.url", settings.postgres_url)

# Add custom logic to handle the creation of the `updated_at` function and trigger for all tables
# IMPORTANT: These SQL operations are Postgres-specific and may not work with other databases.
#            If you a different database is used, you will need to modify this logic accordingly.
def process_revision_directives(context: Any, revision: str | None, directives: List[Any]) -> None:
    migration_script = directives[0]
    upgrade_ops = migration_script.upgrade_ops.ops
    downgrade_ops = migration_script.downgrade_ops.ops
    affected_tables: set[str] = set()

    # Helper functions
    def create_trigger_sql(table_name: str) -> str:
        return clean_multiline_string(f"""
        CREATE TRIGGER update_timestamp
        BEFORE UPDATE ON {table_name}
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
        """)

    def drop_trigger_sql(table_name: str) -> str:
        return f"DROP TRIGGER IF EXISTS update_timestamp ON {table_name};"

    # First collect affected tables
    for op_ in upgrade_ops:
        if isinstance(op_, ops.ModifyTableOps):
            for op in op_.ops:
                if isinstance(op, ops.AddColumnOp) and op.column.name == 'updated_at':
                    affected_tables.add(op_.table_name)
        elif isinstance(op_, ops.CreateTableOp):
            for column in op_.columns:
                if column.name == 'updated_at': # type: ignore
                    affected_tables.add(op_.table_name)

    # Only create function and triggers if we found affected tables
    if affected_tables:
        # Create function first
        upgrade_ops.insert(
            0,
            ops.ExecuteSQLOp(clean_multiline_string("""
            CREATE OR REPLACE FUNCTION set_updated_at()
            RETURNS trigger AS $$
            BEGIN
                NEW.updated_at = timezone('utc', now());
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """))
        )

        # Add triggers for all affected tables
        for table_name in affected_tables:
            upgrade_ops.append(ops.ExecuteSQLOp(create_trigger_sql(table_name)))
            downgrade_ops.append(ops.ExecuteSQLOp(drop_trigger_sql(table_name)))

        # Add drop function in downgrade if any tables were affected
        #(actually, don't do this, as other tables may still need the function)
        # downgrade_ops.append(
        #     ops.ExecuteSQLOp("DROP FUNCTION IF EXISTS set_updated_at();")
        # )

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
        url=settings.postgres_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=settings.postgres_url,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,  # type: ignore
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
