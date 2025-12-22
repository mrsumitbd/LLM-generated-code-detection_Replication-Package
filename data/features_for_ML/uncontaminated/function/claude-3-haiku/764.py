from typing import Annotated
from pydantic import Field

def run_query_tool(
        statement: Annotated[
            str,
            Field(description="SQL query to execute"),
        ],
    ):
    """
    Executes the provided SQL query and returns the result.

    Args:
        statement (str): The SQL query to execute.

    Returns:
        The result of the SQL query execution.
    """
    # Connect to the database
    conn = connect_to_database()

    # Execute the SQL query
    cursor = conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()

    # Close the database connection
    conn.close()

    return result