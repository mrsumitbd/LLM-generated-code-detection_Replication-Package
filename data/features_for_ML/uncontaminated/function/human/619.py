from alembic.config import Config as AlembicConfig
from alembic import command
from sqlalchemy import Engine, text

def upgrade_database(
    alembic_cfg: AlembicConfig, engine: Engine, target_version: str = "head"
) -> None:
    """Upgrade database to target version.

    Args:
        alembic_cfg: alembic config
        engine: sqlalchemy engine
        target_version: target version, default is head(latest version)
    """
    # 开启 SQL 输出 - 添加这行代码
    alembic_cfg.set_main_option('show_sql', 'true')

    # 提高日志级别（可选）
    alembic_cfg.set_main_option('log_level', 'INFO')

    with engine.connect() as connection:
        alembic_cfg.attributes["connection"] = connection
        # Will create tables if not exists
        command.upgrade(alembic_cfg, target_version)