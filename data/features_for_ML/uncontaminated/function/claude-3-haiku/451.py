def process_statement(statement, column_names=[]):
    """
    Processes a SQL statement and returns a list of dictionaries representing the result set.

    Args:
        statement (str): The SQL statement to be processed.
        column_names (list, optional): A list of column names to be used as keys in the result set dictionaries. If not provided, the column names will be automatically generated.

    Returns:
        list: A list of dictionaries representing the result set.
    """
    import sqlite3

    # Connect to an in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    try:
        # Execute the SQL statement
        cursor.execute(statement)

        # Get the column names if not provided
        if not column_names:
            column_names = [description[0] for description in cursor.description]

        # Fetch the result set and convert it to a list of dictionaries
        result_set = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    finally:
        # Close the database connection
        conn.close()

    return result_set