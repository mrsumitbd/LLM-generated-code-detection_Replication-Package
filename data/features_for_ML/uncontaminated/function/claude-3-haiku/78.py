def do_run_migrations(connection: Connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS posts (id SERIAL PRIMARY KEY, title VARCHAR(255), content TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS comments (id SERIAL PRIMARY KEY, content TEXT, post_id INTEGER, user_id INTEGER, FOREIGN KEY (post_id) REFERENCES posts(id), FOREIGN KEY (user_id) REFERENCES users(id))")
        connection.commit()