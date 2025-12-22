def _fetch_table_data(table_name: str, _conn: sqlite3.Connection) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, _conn)