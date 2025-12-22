import sqlite3
import os

DB_FILE = 'database.db'

def populate_database(db_file=DB_FILE):
    """Creates and populates the SQLite database."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Create the table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

    # Insert sample data
    users = [
        ('John Doe', 'john.doe@example.com'),
        ('Jane Smith', 'jane.smith@example.com'),
        ('Bob Johnson', 'bob.johnson@example.com')
    ]
    c.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)

    conn.commit()
    conn.close()

    print(f"Database file created/updated: {os.path.abspath(db_file)}")