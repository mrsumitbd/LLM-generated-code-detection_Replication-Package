import os
import pathlib
from datetime import datetime
from typing import List

from sqlalchemy import text, Table, Column, Integer, String, DateTime, MetaData, select
from sqlalchemy.engine import Connection


def _ensure_migrations_table(conn: Connection) -> None:
    """Create the migrations table if it does not exist."""
    conn.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                applied_at DATETIME NOT NULL
            )
            """
        )
    )


def _get_applied_migrations(conn: Connection) -> List[str]:
    """Return a list of migration names that have already been applied."""
    result = conn.execute(text("SELECT name FROM migrations"))
    return [row[0] for row in result.fetchall()]


def _get_migration_files() -> List[pathlib.Path]:
    """Return a sorted list of migration .sql files in the migrations directory."""
    migrations_dir = pathlib.Path(__file__).parent / "migrations"
    if not migrations_dir.is_dir():
        return []
    files = sorted(
        f for f in migrations_dir.iterdir() if f.is_file() and f.suffix == ".sql"
    )
    return files


def _apply_migration(conn: Connection, migration_path: pathlib.Path) -> None:
    """Apply a single migration file and record it."""
    with migration_path.open("r", encoding="utf-8") as f:
        sql = f.read()

    # Execute the migration SQL
    conn.execute(text(sql))

    # Record the migration
    conn.execute(
        text(
            """
            INSERT INTO migrations (name, applied_at)
            VALUES (:name, :applied_at)
            """
        ),
        {"name": migration_path.name, "applied_at": datetime.utcnow()},
    )


def do_run_migrations(connection: Connection) -> None:
    """
    Run all pending SQL migrations located in the `migrations` directory.

    The function ensures a `migrations` table exists, determines which
    migration files have not yet been applied, applies them in order,
    and records each applied migration.
    """
    # Ensure the migrations table exists
    _ensure_migrations_table(connection)

    # Get the set of already applied migration names
    applied = set(_get_applied_migrations(connection))

    # Get all migration files
    migration_files = _get_migration_files()

    # Apply each pending migration
    for migration_path in migration_files:
        if migration_path.name in applied:
            continue

        # Use a transaction for each migration
        with connection.begin():
            _apply_migration(connection, migration_path)