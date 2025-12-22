import sqlite3

def load_hourly_caps() -> Dict[str, Dict[str, int]]:
    """
    Load hourly API caps from the database

    Returns:
        Dictionary containing hourly API usage for each app
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT app_name, endpoint, cap FROM api_caps")
    result = cursor.fetchall()

    hourly_caps = {}
    for app_name, endpoint, cap in result:
        if app_name not in hourly_caps:
            hourly_caps[app_name] = {}
        hourly_caps[app_name][endpoint] = cap

    conn.close()
    return hourly_caps