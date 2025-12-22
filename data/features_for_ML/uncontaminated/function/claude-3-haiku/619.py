def upgrade_database(
    alembic_cfg: AlembicConfig, engine: Engine, target_version: str = "head"
) -> None:
    """Upgrade database to target version.

    Args:
        alembic_cfg: alembic config
        engine: sqlalchemy engine
        target_version: target version, default is head(latest version)
    """
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        alembic_command.upgrade(alembic_cfg, target_version)