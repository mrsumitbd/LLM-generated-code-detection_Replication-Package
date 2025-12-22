def verify_stored_procedures(conn) -> bool:
    """Verify that stored procedure was created."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = DATABASE()")
            procedures = cursor.fetchall()
            if procedures:
                return True
            else:
                return False
    except Exception as e:
        print(f"Error verifying stored procedures: {e}")
        return False