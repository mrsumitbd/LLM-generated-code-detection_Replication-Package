from typing import Annotated
from pydantic import Field
import sqlite3
import os
import json

def run_query_tool(
    statement: Annotated[
        str,
        Field(description="SQL query to execute"),
    ],
):
    """
    Execute a SQL query against a SQLite database and return the results as a JSON string.

    The database file is expected to be located at the path specified by the
    environment variable `SQLITE_DB_PATH`. If the variable is not set, the
    function will default to `database.db` in the current working directory.

    Parameters
    ----------
    statement : str
        The SQL query to execute.

    Returns
    -------
    str
        A JSON string containing either the query results or an error message.
    """
    # Determine the database path
    db_path = os.getenv("SQLITE_DB_PATH", "database.db")

    # Ensure the database file exists
    if not os.path.exists(db_path):
        return json.dumps(
            {
                "error": f"Database file not found at '{db_path}'.",
                "statement": statement,
            }
        )

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(statement)
            # If the query returns rows (e.g., SELECT)
            if cursor.description:
                rows = cursor.fetchall()
                # Convert rows to list of dicts
                result = [dict(row) for row in rows]
                return json.dumps(
                    {
                        "rows": result,
                        "rowcount": cursor.rowcount,
                        "statement": statement,
                    },
                    default=str,
                )
            else:
                # For queries that don't return rows (e.g., INSERT, UPDATE)
                conn.commit()
                return json.dumps(
                    {
                        "message": "Query executed successfully.",
                        "rowcount": cursor.rowcount,
                        "statement": statement,
                    }
                )
    except sqlite3.Error as e:
        return json.dumps(
            {
                "error": str(e),
                "statement": statement,
            }
        )