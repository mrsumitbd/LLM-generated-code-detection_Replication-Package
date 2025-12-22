import os
from alembic import command
from alembic.config import Config
from sqlalchemy import Connection

def do_run_migrations(connection: Connection) -> None:
    """Run database migrations using Alembic."""
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(connection.engine.url))
    
    with connection.begin():
        config.attributes["connection"] = connection
        command.upgrade(config, "head")