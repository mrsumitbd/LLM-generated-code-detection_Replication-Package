def do_run_migrations(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(100))")
    connection.commit()
    cursor.close()