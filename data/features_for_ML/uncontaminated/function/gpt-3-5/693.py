import sqlite3

DB_FILE = 'mydatabase.db'

def populate_database(db_file=DB_FILE):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    c.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
    c.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
    c.execute("INSERT INTO users (name, age) VALUES ('Charlie', 35)")

    conn.commit()
    conn.close()