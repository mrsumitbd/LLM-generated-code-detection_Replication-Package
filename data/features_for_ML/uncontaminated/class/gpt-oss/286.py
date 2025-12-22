import sqlite3
from typing import Any, List, Optional

class DBConn:
    def __init__(self, db_service: Any):
        """
        Initialize the DBConn with a DBService instance.

        Parameters
        ----------
        db_service : Any
            An object that provides database connection information.
            It may expose a `get_connection()` method that returns a DB-API
            connection object, or it may provide a `database` attribute
            (e.g., a SQLite file path) that can be used with sqlite3.
        """
        self.db_service = db_service
        self.conn: Optional[Any] = None

    def connect(self) -> Any:
        """
        Create and return a database connection.

        Returns
        -------
        Any
            A DB-API connection object.
        """
        if self.conn is None:
            # Prefer a custom get_connection() method if available
            if hasattr(self.db_service, "get_connection") and callable(self.db_service.get_connection):
                self.conn = self.db_service.get_connection()
            else:
                # Fallback to sqlite3 using a `database` attribute
                db_path = getattr(self.db_service, "database", ":memory:")
                self.conn = sqlite3.connect(db_path)
        return self.conn

    def close(self) -> None:
        """
        Close the database connection if it is open.
        """
        if self.conn:
            try:
                self.conn.close()
            finally:
                self.conn = None

    def execute_sql(self, sql: str) -> Optional[List[Any]]:
        """
        Execute a SQL statement and return the fetched results.

        Parameters
        ----------
        sql : str
            The SQL query to execute.

        Returns
        -------
        Optional[List[Any]]
            The fetched rows if the query returns data; otherwise None.
        """
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            # Attempt to fetch results; if the statement doesn't return rows,
            # fetchall() will raise an exception which we ignore.
            try:
                return cursor.fetchall()
            except Exception:
                return None
        finally:
            cursor.close()