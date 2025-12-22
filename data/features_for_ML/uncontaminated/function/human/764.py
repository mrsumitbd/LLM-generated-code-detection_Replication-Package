from typing import Annotated
from pydantic import Field

def run_query_tool(
        statement: Annotated[
            str,
            Field(description="SQL query to execute"),
        ],
    ):
        return run_query(statement, snowflake_service)