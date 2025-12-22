class ExplainPlanTool:
    """Tool for generating and analyzing PostgreSQL explain plans."""

    def __init__(self, sql_driver: SqlDriver):
        self.sql_driver = sql_driver

    def _has_bind_variables(self, query: str) -> bool:
        """Check if query contains bind variables (e.g., :param, $1, ?, @param)."""
        import re
        # Check for common bind variable patterns
        patterns = [
            r':\w+',           # :param_name
            r'\$\d+',          # $1, $2, etc.
            r'\?',              # ? placeholder
            r'@\w+',           # @param_name
        ]
        for pattern in patterns:
            if re.search(pattern, query):
                return True
        return False

    def _has_like_expressions(self, query: str) -> bool:
        """Check if query contains LIKE expressions with wildcards."""
        import re
        # Check for LIKE keyword followed by string patterns with wildcards
        pattern = r'\bLIKE\s+[\'"]%.*?[\'"]|\bLIKE\s+[\'"].*?%[\'"]'
        return bool(re.search(pattern, query, re.IGNORECASE))