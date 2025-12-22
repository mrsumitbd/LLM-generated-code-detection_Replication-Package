import sqlite3
from typing import List

def get_database_tables(db: str) -> str:
    """
    Return a comma‑separated string of table names in the given SQLite database file.
    If the database cannot be opened or contains no tables, an empty string is returned.
    """
    if not db:
        return ""

    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        rows: List[tuple] = cursor.fetchall()
        conn.close()
    except Exception:
        return ""

    table_names = [row[0] for row in rows]
    return ", ".join(table_names)