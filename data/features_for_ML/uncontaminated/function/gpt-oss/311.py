from __future__ import annotations

import os
import re
from typing import List, Optional, Union

import snowflake.connector
from pydantic import Field
from typing_extensions import Annotated

# The type annotation for object_type is expected to be a string literal
# representing a Snowflake object type such as "TABLE", "VIEW", "WAREHOUSE", etc.
object_type_annotation = str


def list_objects_tool(
    object_type: object_type_annotation,
    database_name: str | None = None,
    schema_name: str | None = None,
    like: Annotated[
        str | None,
        Field(
            description="Filter objects by keyword in name. Uses case-insensitive pattern matching, with support for SQL wildcard characters (% and _).",
            default=None,
        ),
    ] = None,
    starts_with: Annotated[
        str | None,
        Field(
            description="Filter objects by start of name. Case sensitive. Ignored for warehouses.",
            default=None,
        ),
    ] = None,
) -> List[str]:
    """
    List Snowflake objects of a given type, optionally filtered by database, schema,
    a case-insensitive LIKE pattern, or a case-sensitive starts-with prefix.

    Parameters
    ----------
    object_type : str
        The type of object to list (e.g., "TABLE", "VIEW", "WAREHOUSE").
    database_name : str | None
        Optional database name to restrict the search to.
    schema_name : str | None
        Optional schema name to restrict the search to.
    like : str | None
        Optional case-insensitive pattern to filter object names.
    starts_with : str | None
        Optional case-sensitive prefix to filter object names. Ignored for warehouses.

    Returns
    -------
    List[str]
        A list of object names that match the criteria.
    """
    # Validate object_type
    valid_types = {"TABLE", "VIEW", "WAREHOUSE", "SCHEMA", "DATABASE"}
    if object_type.upper() not in valid_types:
        raise ValueError(f"Unsupported object_type '{object_type}'. Supported types: {valid_types}")

    # Build the base query
    if object_type.upper() == "WAREHOUSE":
        # Warehouses are listed via SHOW WAREHOUSES
        base_query = "SHOW WAREHOUSES"
    else:
        # For tables and views, use the information_schema
        base_query = f"SELECT table_name FROM information_schema.{object_type.lower()}s"

    # Build WHERE clauses
    where_clauses = []

    if database_name:
        if object_type.upper() == "WAREHOUSE":
            # SHOW WAREHOUSES does not support filtering by database
            pass
        else:
            where_clauses.append(f"table_catalog = '{database_name}'")

    if schema_name:
        if object_type.upper() == "WAREHOUSE":
            pass
        else:
            where_clauses.append(f"table_schema = '{schema_name}'")

    if like:
        # Escape % and _ in the pattern for LIKE
        escaped_like = re.escape(like).replace(r"\%", "%").replace(r"\_", "_")
        if object_type.upper() == "WAREHOUSE":
            # SHOW WAREHOUSES does not support LIKE directly; we will filter after fetch
            pass
        else:
            where_clauses.append(f"table_name ILIKE '%{escaped_like}%'")

    if starts_with and object_type.upper() != "WAREHOUSE":
        where_clauses.append(f"table_name LIKE '{starts_with}%'")

    if where_clauses:
        if object_type.upper() == "WAREHOUSE":
            # No WHERE clause for SHOW WAREHOUSES; we will filter after fetch
            pass
        else:
            base_query += " WHERE " + " AND ".join(where_clauses)

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )
    cur = conn.cursor()
    try:
        cur.execute(base_query)
        rows = cur.fetchall()
        # Extract names
        if object_type.upper() == "WAREHOUSE":
            # SHOW WAREHOUSES returns a tuple with many columns; name is the 2nd column
            names = [row[1] for row in rows]
        else:
            names = [row[0] for row in rows]

        # Apply LIKE and starts_with filters for warehouses (since SHOW does not support them)
        if object_type.upper() == "WAREHOUSE":
            if like:
                pattern = re.compile(like.replace("%", ".*").replace("_", "."), re.IGNORECASE)
                names = [n for n in names if pattern.search(n)]
            if starts_with:
                names = [n for n in names if n.startswith(starts_with)]

        return names
    finally:
        cur.close()
        conn.close()