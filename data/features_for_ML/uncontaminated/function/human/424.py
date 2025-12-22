def verify_stored_procedures(conn) -> bool:
    """Verify that stored procedure was created."""
    with conn.cursor() as cur:
        # Check if procedure exists
        cur.execute("""
            SELECT routine_name FROM information_schema.routines 
            WHERE routine_schema = 'employees' 
            AND routine_type = 'FUNCTION'
            AND routine_name = 'generate_monthly_report'
        """)
        procedures = [row[0] for row in cur.fetchall()]
        
        if 'generate_monthly_report' not in procedures:
            print("❌ generate_monthly_report procedure not found")
            return False
            
        # Check if monthly_reports table exists with correct structure
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = 'employees' AND table_name = 'monthly_reports'
            AND column_name IN ('report_id', 'report_date', 'department_count', 'total_employees', 'avg_salary', 'generated_at')
        """)
        report_columns = cur.fetchone()[0]
        if report_columns != 6:
            print("❌ monthly_reports table missing required columns")
            return False
            
        print("✅ Stored procedure and supporting table are created")
        return True