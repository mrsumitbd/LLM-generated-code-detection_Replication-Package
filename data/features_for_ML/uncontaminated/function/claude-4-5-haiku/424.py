def verify_stored_procedures(conn) -> bool:
    """Verify that stored procedure was created."""
    try:
        cursor = conn.cursor()
        
        # Query to check if stored procedures exist
        # This works for SQL Server
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_TYPE = 'PROCEDURE'
        """)
        
        result = cursor.fetchone()
        cursor.close()
        
        # If there's at least one stored procedure, return True
        return result[0] > 0 if result else False
    except Exception:
        return False