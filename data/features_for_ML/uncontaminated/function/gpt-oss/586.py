import sqlite3
import os

def connect():
    """
    Establishes and returns a connection to a SQLite database named 'example.db'.
    If the database file does not exist, it will be created automatically.
    """
    db_path = os.path.join(os.path.dirname(__file__), "example.db")
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to connect to the database: {e}") from e