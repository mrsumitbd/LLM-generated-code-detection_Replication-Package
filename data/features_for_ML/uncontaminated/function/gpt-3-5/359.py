def create_alembic_config(
    alembic_root_path: str,
    engine: Engine,
    base: DeclarativeMeta,
    session: Session,
    alembic_ini_path: Optional[str] = None,
    script_location: Optional[str] = None,
) -> AlembicConfig:
    from alembic.config import Config
    from alembic import context

    config = Config()
    config.set_main_option('script_location', script_location or alembic_root_path)
    config.set_main_option('sqlalchemy.url', str(engine.url))
    config.set_main_option('sqlalchemy.engine', str(engine))
    config.set_main_option('target_metadata', base.metadata)
    config.attributes['connection'] = engine.connect()
    config.attributes['target_metadata'] = base.metadata
    config.attributes['alembic_script_location'] = script_location or alembic_root_path
    config.attributes['alembic_ini_path'] = alembic_ini_path

    def run_migrations_offline():
        context.configure(
            url=engine.url,
            target_metadata=base.metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online():
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=base.metadata,
                process_revision_directives=process_revision_directives,
            )

            with context.begin_transaction():
                context.run_migrations()

    if alembic_ini_path:
        config.set_main_option('script_location', script_location or alembic_root_path)
        context.configure(
            config=config,
            target_metadata=base.metadata,
            process_revision_directives=process_revision_directives,
        )
    else:
        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()

    return config