import sqlite3

def connect():
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None