def populate_database(db_file=DB_FILE):
    """Creates and populates the SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Insert sample data
    sample_users = [
        ('alice', 'alice@example.com', 'hashed_password_1'),
        ('bob', 'bob@example.com', 'hashed_password_2'),
        ('charlie', 'charlie@example.com', 'hashed_password_3'),
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, email, password) VALUES (?, ?, ?)',
        sample_users
    )
    
    sample_posts = [
        (1, 'First Post', 'This is my first post'),
        (1, 'Second Post', 'Another interesting post'),
        (2, 'Hello World', 'Getting started with databases'),
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO posts (user_id, title, content) VALUES (?, ?, ?)',
        sample_posts
    )
    
    sample_comments = [
        (1, 2, 'Great post!'),
        (1, 1, 'Thanks for sharing'),
        (2, 3, 'Very helpful'),
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO comments (post_id, user_id, content) VALUES (?, ?, ?)',
        sample_comments
    )
    
    conn.commit()
    conn.close()