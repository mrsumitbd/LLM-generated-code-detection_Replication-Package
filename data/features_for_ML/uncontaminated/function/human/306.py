import sqlalchemy

def _format_index(index: sqlalchemy.engine.interfaces.ReflectedIndex) -> str:
    return (
        f"Name: {index['name']}, Unique: {index['unique']},"
        f" Columns: {str(index['column_names'])}"
    )