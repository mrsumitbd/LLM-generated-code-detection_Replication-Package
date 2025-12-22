import sqlite3

def get_database_tables(db: str) -> str:
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = ", ".join([table[0] for table in tables])
        return table_names
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        if conn:
            conn.close()