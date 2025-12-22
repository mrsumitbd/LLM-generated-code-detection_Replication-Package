from typing import Annotated
from pydantic import Field
import sqlite3

def run_query_tool(
        statement: Annotated[
            str,
            Field(description="SQL query to execute"),
        ],
    ):
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute(statement)
        
        if statement.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            conn.close()
            return {
                "success": True,
                "columns": columns,
                "rows": results,
                "row_count": len(results)
            }
        else:
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            return {
                "success": True,
                "affected_rows": affected_rows,
                "message": f"Query executed successfully. {affected_rows} rows affected."
            }
    except sqlite3.Error as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Database error occurred"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "An unexpected error occurred"
        }