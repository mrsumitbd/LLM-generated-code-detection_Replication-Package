class ExplainPlanTool:
    """Tool for generating and analyzing PostgreSQL explain plans."""

    def __init__(self, sql_driver: SqlDriver):
        self.sql_driver = sql_driver

    def _has_bind_variables(self, query: str) -> bool:
        return ':' in query

    def _has_like_expressions(self, query: str) -> bool:
        return 'LIKE' in query.upper()