import sqlite3
import pandas as pd

def _fetch_table_data(table_name: str, _conn: sqlite3.Connection) -> pd.DataFrame:
    cur = _conn.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)

    return df