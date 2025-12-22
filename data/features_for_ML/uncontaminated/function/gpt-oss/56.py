import pandas as pd
import sqlite3

def _fetch_table_data(table_name: str, _conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Fetch all rows from the specified table in the given SQLite connection and return them as a pandas DataFrame.

    Parameters
    ----------
    table_name : str
        Name of the table to fetch data from.
    _conn : sqlite3.Connection
        SQLite connection object.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all rows from the table.

    Raises
    ------
    sqlite3.Error
        If the table does not exist or another SQLite error occurs.
    """
    # Ensure the table name is safe by quoting it with double quotes
    # This prevents SQL injection for table names that might contain special characters.
    query = f'SELECT * FROM "{table_name}"'
    try:
        df = pd.read_sql_query(query, _conn)
    except sqlite3.Error as e:
        # Re-raise the exception with a more informative message
        raise sqlite3.Error(f"Error fetching data from table '{table_name}': {e}") from e
    return df