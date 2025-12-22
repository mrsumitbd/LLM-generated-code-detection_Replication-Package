import sqlite3
import datetime
from pathlib import Path

# Default database file path (can be overridden by the caller)
DB_FILE = Path(__file__).parent / "app.db"

def populate_database(db_file=DB_FILE):
    """Creates and populates the SQLite database."""
    # Ensure the directory exists
    db_file = Path(db_file)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
        """
    )

    # Helper to check if a table is empty
    def table_empty(table_name):
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0] == 0

    # Populate users
    if table_empty("users"):
        now = datetime.datetime.utcnow().isoformat()
        users = [
            ("Alice Smith", "alice@example.com", now),
            ("Bob Johnson", "bob@example.com", now),
            ("Carol Williams", "carol@example.com", now),
        ]
        cursor.executemany(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)", users
        )

    # Populate tags
    if table_empty("tags"):
        tags = [("python",), ("sqlite",), ("tutorial",), ("blog",)]
        cursor.executemany("INSERT INTO tags (name) VALUES (?)", tags)

    # Populate posts
    if table_empty("posts"):
        # Retrieve user ids
        cursor.execute("SELECT id FROM users ORDER BY id")
        user_ids = [row[0] for row in cursor.fetchall()]

        now = datetime.datetime.utcnow().isoformat()
        posts = [
            (user_ids[0], "First Post", "This is the first post content.", now),
            (user_ids[1], "Second Post", "This is the second post content.", now),
            (user_ids[2], "Third Post", "This is the third post content.", now),
            (user_ids[0], "Another Post", "More content here.", now),
            (user_ids[1], "Yet Another Post", "Even more content.", now),
        ]
        cursor.executemany(
            "INSERT INTO posts (user_id, title, content, created_at) VALUES (?, ?, ?, ?)",
            posts,
        )

    # Populate post_tags
    if table_empty("post_tags"):
        # Map tag names to ids
        cursor.execute("SELECT id, name FROM tags")
        tag_map = {name: tid for tid, name in cursor.fetchall()}

        # Map post titles to ids
        cursor.execute("SELECT id, title FROM posts")
        post_map = {title: pid for pid, title in cursor.fetchall()}

        post_tags = [
            (post_map["First Post"], tag_map["python"]),
            (post_map["First Post"], tag_map["tutorial"]),
            (post_map["Second Post"], tag_map["sqlite"]),
            (post_map["Second Post"], tag_map["blog"]),
            (post_map["Third Post"], tag_map["python"]),
            (post_map["Third Post"], tag_map["blog"]),
            (post_map["Another Post"], tag_map["tutorial"]),
            (post_map["Yet Another Post"], tag_map["sqlite"]),
        ]
        cursor.executemany(
            "INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", post_tags
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()