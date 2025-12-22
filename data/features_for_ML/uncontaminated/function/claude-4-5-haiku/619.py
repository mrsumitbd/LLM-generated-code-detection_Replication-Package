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
        alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
        context = MigrationContext.configure(connection)
        alembic_cfg.attributes["connection"] = connection
        
        with EnvironmentContext(alembic_cfg, context) as env_context:
            env_context.configure(
                connection=connection,
                target_metadata=None
            )
            with env_context.begin_transaction():
                env_context.run_migrations()