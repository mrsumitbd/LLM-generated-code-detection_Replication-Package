import datetime
import uuid

def add_history_entry(app_type, entry_data):
    """
    Add a history entry for processed media
    
    Parameters:
    - app_type: str - The app type (sonarr, radarr, etc)
    - entry_data: dict - Entry data containing id, name, operation_type, instance_name
    
    Returns:
    - dict - The created history entry or None if failed
    """
    try:
        history_entry = {
            "id": str(uuid.uuid4()),
            "app_type": app_type,
            "name": entry_data["name"],
            "operation_type": entry_data["operation_type"],
            "instance_name": entry_data["instance_name"],
            "timestamp": datetime.datetime.now().isoformat()
        }
        return history_entry
    except Exception:
        return None