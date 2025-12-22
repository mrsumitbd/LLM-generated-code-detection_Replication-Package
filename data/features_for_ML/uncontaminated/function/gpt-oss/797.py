from __future__ import annotations

import os
import sqlite3
from collections import defaultdict
from typing import Dict

def load_hourly_caps() -> Dict[str, Dict[str, int]]:
    """
    Load hourly API caps from the database.

    The function expects a SQLite database file whose path can be
    overridden by the environment variable `CAPS_DB`.  The database
    must contain a table named `hourly_caps` with the following
    columns:

        - app_id   TEXT   -- Identifier for the application
        - hour     TEXT   -- Hour identifier (e.g. "2024-11-20T14:00:00Z")
        - cap      INTEGER

    The function returns a nested dictionary mapping each `app_id`
    to a dictionary that maps `hour` to the corresponding `cap`.

    If the database file does not exist, the table is missing, or
    any other error occurs, an empty dictionary is returned.
    """
    db_path = os.getenv("CAPS_DB", "caps.db")
    caps: Dict[str, Dict[str, int]] = defaultdict(dict)

    if not os.path.exists(db_path):
        return {}

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT app_id, hour, cap
            FROM hourly_caps
            """
        )
        rows = cur.fetchall()
        for app_id, hour, cap in rows:
            caps[app_id][hour] = int(cap)
    except sqlite3.Error:
        # If any SQLite error occurs (e.g., table missing), return empty dict
        return {}
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return dict(caps)