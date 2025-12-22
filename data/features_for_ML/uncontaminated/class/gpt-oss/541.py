import re
from typing import Any

class ExplainPlanTool:
    """Tool for generating and analyzing PostgreSQL explain plans."""

    def __init__(self, sql_driver: Any):
        """
        Initialize the ExplainPlanTool with a SQL driver.

        Parameters
        ----------
        sql_driver : Any
            An object that provides a `cursor()` method returning a cursor
            with an `execute()` method that accepts a SQL string and optional
            parameters.
        """
        self.sql_driver = sql_driver

    def _has_bind_variables(self, query: str) -> bool:
        """
        Detect if the query contains bind variable placeholders.

        PostgreSQL uses $1, $2, ... for positional parameters.
        Some drivers also support %s placeholders.

        Parameters
        ----------
        query : str
            The SQL query string.

        Returns
        -------
        bool
            True if bind variable placeholders are present, False otherwise.
        """
        # Positional placeholders: $1, $2, etc.
        if re.search(r'\$\d+', query):
            return True
        # Common placeholder for DB-API: %s
        if re.search(r'%s', query):
            return True
        return False

    def _has_like_expressions(self, query: str) -> bool:
        """
        Detect if the query contains LIKE or ILIKE expressions.

        Parameters
        ----------
        query : str
            The SQL query string.

        Returns
        -------
        bool
            True if LIKE or ILIKE expressions are present, False otherwise.
        """
        # Case-insensitive search for LIKE or ILIKE
        return bool(re.search(r'\bLIKE\b|\bILIKE\b', query, re.IGNORECASE))