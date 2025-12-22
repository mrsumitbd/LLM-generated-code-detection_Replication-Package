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
    if alembic_ini_path is None:
        alembic_ini_path = os.path.join(alembic_root_path, "alembic.ini")
    
    if script_location is None:
        script_location = os.path.join(alembic_root_path, "versions")
    
    config = AlembicConfig(alembic_ini_path)
    config.set_main_option("sqlalchemy.url", str(engine.url))
    config.set_main_option("script_location", script_location)
    
    config.attributes["sqlalchemy.engine"] = engine
    config.attributes["sqlalchemy.session"] = session
    config.attributes["sqlalchemy.base"] = base
    
    return config