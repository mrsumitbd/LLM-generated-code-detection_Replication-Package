def upgrade_database(
    alembic_cfg: AlembicConfig, engine: Engine, target_version: str = "head"
) -> None:
    from alembic import command
    command.upgrade(alembic_cfg, target_version)