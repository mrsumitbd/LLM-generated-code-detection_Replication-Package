import sqlite3
from typing import Iterable, List, Optional, Sequence, Union


class CommandGetTableTypes:
    """Represents a command that retrieves the supported table types from a database.

    The command works with any DB‑API 2.0 compatible connection.  For SQLite it
    queries ``sqlite_master``; for other databases it falls back to the
    ``information_schema.tables`` view.  The result is a list of unique table
    type names (e.g. ``TABLE``, ``VIEW``).

    Parameters
    ----------
    connection : object
        A DB‑API 2.0 connection object.  It must provide a ``cursor`` method
        that returns a cursor supporting ``execute`` and ``fetchall``.
    """

    def __init__(self, connection: object) -> None:
        self._connection = connection
        self._cursor: Optional[object] = None
        self._result: Optional[List[str]] = None

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def execute(self) -> List[str]:
        """Execute the command and return the list of table types.

        Returns
        -------
        list[str]
            The unique table type names supported by the database.
        """
        self._close_cursor()
        self._cursor = self._connection.cursor()

        # Try SQLite first
        try:
            self._cursor.execute("SELECT DISTINCT type FROM sqlite_master")
            rows = self._cursor.fetchall()
            self._result = [row[0] for row in rows]
        except Exception:
            # Fallback to generic SQL standard
            try:
                self._cursor.execute(
                    "SELECT DISTINCT table_type FROM information_schema.tables"
                )
                rows = self._cursor.fetchall()
                self._result = [row[0] for row in rows]
            except Exception as exc:
                self._result = []
                raise RuntimeError("Unable to retrieve table types") from exc

        return self._result

    def fetch(self) -> Optional[List[str]]:
        """Return the result of the last :meth:`execute` call.

        Returns
        -------
        list[str] | None
            The list of table types, or ``None`` if :meth:`execute` has not
            been called yet.
        """
        return self._result

    # --------------------------------------------------------------------- #
    # Convenience helpers
    # --------------------------------------------------------------------- #
    @property
    def result(self) -> Optional[List[str]]:
        """Alias for :meth:`fetch`."""
        return self.fetch()

    def __repr__(self) -> str:
        return f"<CommandGetTableTypes result={self._result!r}>"

    # --------------------------------------------------------------------- #
    # Cleanup
    # --------------------------------------------------------------------- #
    def _close_cursor(self) -> None:
        if self._cursor is not None:
            try:
                self._cursor.close()
            finally:
                self._cursor = None

    def __del__(self) -> None:
        self._close_cursor()