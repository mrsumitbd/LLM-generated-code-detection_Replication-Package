from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.session import Session

def create_alembic_config(
    alembic_root_path: str,
    engine: Engine,
    base: DeclarativeMeta,
    session: Session,
    alembic_ini_path: Optional[str] = None,
    script_location: Optional[str] = None,
) -> AlembicConfig:
    config = Config(alembic_ini_path or f"{alembic_root_path}/alembic.ini")
    config.set_main_option("script_location", script_location or f"{alembic_root_path}/alembic")
    config.set_main_option("sqlalchemy.url", str(engine.url))
    config.attributes["engine"] = engine
    config.attributes["base"] = base
    config.attributes["session"] = session
    return config