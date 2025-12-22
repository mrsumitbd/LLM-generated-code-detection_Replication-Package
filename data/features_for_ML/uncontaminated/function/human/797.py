from src.primary.utils.database import get_database
from typing import Dict, Any, Optional

def load_hourly_caps() -> Dict[str, Dict[str, int]]:
    """
    Load hourly API caps from the database
    
    Returns:
        Dictionary containing hourly API usage for each app
    """
    try:
        db = get_database()
        caps = db.get_hourly_caps()
        
        # Ensure all apps are in the caps
        default_caps = get_default_hourly_caps()
        for app in default_caps:
            if app not in caps:
                caps[app] = default_caps[app]
        
        return caps
    except Exception as e:
        logger.error(f"Error loading hourly caps from database: {e}")
        return get_default_hourly_caps()