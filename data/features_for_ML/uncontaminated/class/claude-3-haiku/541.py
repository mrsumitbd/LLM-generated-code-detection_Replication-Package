class ExplainPlanTool:
    """Tool for generating and analyzing PostgreSQL explain plans."""

    def __init__(self, sql_driver: SqlDriver):
        self.sql_driver = sql_driver

    def _has_bind_variables(self, query: str) -> bool:
        return '?' in query

    def _has_like_expressions(self, query: str) -> bool:
        return 'LIKE' in query.upper()

    def generate_explain_plan(self, query: str) -> str:
        if self._has_bind_variables(query):
            raise ValueError("Query cannot contain bind variables.")

        if self._has_like_expressions(query):
            raise ValueError("Query cannot contain LIKE expressions.")

        return self.sql_driver.execute_explain(query)

    def analyze_explain_plan(self, explain_plan: str) -> dict:
        # Implement the logic to analyze the explain plan and return a dictionary
        # with relevant metrics and insights.
        pass