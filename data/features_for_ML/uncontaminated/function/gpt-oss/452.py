import datetime

# Simple in-memory history store (optional)
_history_entries = []

def add_history_entry(app_type, entry_data):
    """
    Add a history entry for processed media
    
    Parameters:
    - app_type: str - The app type (sonarr, radarr, etc)
    - entry_data: dict - Entry data containing id, name, operation_type, instance_name
    
    Returns:
    - dict - The created history entry or None if failed
    """
    # Validate required keys
    required_keys = {"id", "name", "operation_type", "instance_name"}
    if not isinstance(entry_data, dict) or not required_keys.issubset(entry_data):
        return None

    # Build the history entry
    history_entry = {
        "app_type": app_type,
        "id": entry_data["id"],
        "name": entry_data["name"],
        "operation_type": entry_data["operation_type"],
        "instance_name": entry_data["instance_name"],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Store in the in-memory list (optional)
    _history_entries.append(history_entry)

    return history_entry