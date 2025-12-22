import os
from alembic.config import Config as AlembicConfig
from typing import Optional
from sqlalchemy import Engine, text
from sqlalchemy.orm import DeclarativeMeta, Session

def create_alembic_config(
    alembic_root_path: str,
    engine: Engine,
    base: DeclarativeMeta,
    session: Session,
    alembic_ini_path: Optional[str] = None,
    script_location: Optional[str] = None,
) -> AlembicConfig:
    """Create alembic config.

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
    alembic_ini_path = alembic_ini_path or os.path.join(
        alembic_root_path, "alembic.ini"
    )
    alembic_cfg = AlembicConfig(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    script_location = script_location or os.path.join(alembic_root_path, "alembic")
    versions_dir = os.path.join(script_location, "versions")

    os.makedirs(script_location, exist_ok=True)
    os.makedirs(versions_dir, exist_ok=True)

    alembic_cfg.set_main_option("script_location", script_location)

    alembic_cfg.attributes["target_metadata"] = base.metadata
    alembic_cfg.attributes["session"] = session
    return alembic_cfg