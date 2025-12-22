from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.engine import Engine


def upgrade_database(
    alembic_cfg: AlembicConfig, engine: Engine, target_version: str = "head"
) -> None:
    """
    Upgrade database to target version.

    Args:
        alembic_cfg: Alembic configuration object.
        engine: SQLAlchemy engine connected to the target database.
        target_version: Target migration revision (default is "head").
    """
    # Ensure we use the provided engine for migrations
    connection = engine.connect()
    try:
        # Attach the connection to Alembic's configuration
        alembic_cfg.attributes["connection"] = connection
        # Run the upgrade command
        command.upgrade(alembic_cfg, target_version)
    finally:
        # Clean up the connection
        connection.close()