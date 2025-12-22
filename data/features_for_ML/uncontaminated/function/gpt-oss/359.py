from typing import Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta, Session
from alembic.config import Config as AlembicConfig
import os


def create_alembic_config(
    alembic_root_path: str,
    engine: Engine,
    base: DeclarativeMeta,
    session: Session,
    alembic_ini_path: Optional[str] = None,
    script_location: Optional[str] = None,
) -> AlembicConfig:
    """
    Create alembic config.

    Args:
        alembic_root_path: alembic root path
        engine: sqlalchemy engine
        base: sqlalchemy base
        session: sqlalchemy session
        alembic_ini_path (Optional[str]): alembic ini path
        script_location (Optional[str]): alembic script location

    Returns:
        alembic config
    """
    # Determine the path to the alembic.ini file
    if alembic_ini_path is None:
        alembic_ini_path = os.path.join(alembic_root_path, "alembic.ini")

    # Create the Alembic config object
    cfg = AlembicConfig(alembic_ini_path)

    # Set the script location (folder containing migration scripts)
    if script_location is None:
        script_location = os.path.join(alembic_root_path, "migrations")
    cfg.set_main_option("script_location", script_location)

    # Set the SQLAlchemy URL from the engine
    cfg.set_main_option("sqlalchemy.url", str(engine.url))

    # Optional: set the target metadata for autogenerate
    cfg.set_main_option("target_metadata", base.metadata)

    # Optional: set the session factory if needed
    cfg.set_main_option("session_factory", str(session))

    return cfg