def verify_stored_procedures(conn) -> bool:
    """
    Verify that at least one stored procedure exists in the connected database.
    The function attempts to query the database's information schema for
    routines of type 'PROCEDURE'. It supports both SQLAlchemy connections
    (which expose an `execute` method) and raw DB-API connections (which
    expose a `cursor` method). If any stored procedure is found, the
    function returns True; otherwise it returns False. Any exception
    encountered during the query results in a False return value.
    """
    try:
        # SQLAlchemy connection or Engine
        if hasattr(conn, "execute"):
            # Use the execute method; it returns a ResultProxy or similar
            result = conn.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM information_schema.routines
                WHERE routine_type = 'PROCEDURE'
                """
            )
            # For SQLAlchemy 1.x ResultProxy
            if hasattr(result, "scalar"):
                count = result.scalar()
            else:
                row = result.fetchone()
                count = row[0] if row else 0
            return count > 0

        # Raw DB-API connection (e.g., psycopg2, pymysql)
        if hasattr(conn, "cursor"):
            cur = conn.cursor()
            cur.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM information_schema.routines
                WHERE routine_type = 'PROCEDURE'
                """
            )
            row = cur.fetchone()
            cur.close()
            count = row[0] if row else 0
            return count > 0

    except Exception:
        # Any error (e.g., unsupported dialect, missing schema) results in False
        return False

    # If we reach here, the connection type is unsupported
    return False