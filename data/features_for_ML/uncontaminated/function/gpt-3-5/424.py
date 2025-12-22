def verify_stored_procedures(conn) -> bool:
    cursor = conn.cursor()
    cursor.execute("SHOW PROCEDURE STATUS")
    procedures = cursor.fetchall()
    for procedure in procedures:
        if procedure[1] == 'procedure_name':
            return True
    return False