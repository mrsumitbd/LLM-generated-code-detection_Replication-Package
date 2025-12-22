def load_hourly_caps() -> Dict[str, Dict[str, int]]:
    """
    Load hourly API caps from the database
    
    Returns:
        Dictionary containing hourly API usage for each app
    """
    import sqlite3
    from datetime import datetime, timedelta
    
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hourly_caps (
                app_id TEXT PRIMARY KEY,
                hour TEXT,
                usage_count INTEGER
            )
        ''')
        
        cursor.execute('SELECT app_id, hour, usage_count FROM hourly_caps')
        rows = cursor.fetchall()
        
        hourly_caps = {}
        for app_id, hour, usage_count in rows:
            if app_id not in hourly_caps:
                hourly_caps[app_id] = {}
            hourly_caps[app_id][hour] = usage_count
        
        conn.close()
        return hourly_caps
    
    except Exception:
        return {}