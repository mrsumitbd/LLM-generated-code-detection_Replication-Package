def add_history_entry(app_type, entry_data):
    """
    Add a history entry for processed media
    
    Parameters:
    - app_type: str - The app type (sonarr, radarr, etc)
    - entry_data: dict - Entry data containing id, name, operation_type, instance_name
    
    Returns:
    - dict - The created history entry or None if failed
    """
    import json
    import os
    from datetime import datetime
    
    if not app_type or not entry_data:
        return None
    
    required_fields = ['id', 'name', 'operation_type', 'instance_name']
    if not all(field in entry_data for field in required_fields):
        return None
    
    history_dir = os.path.join(os.path.expanduser('~'), '.media_manager', 'history')
    os.makedirs(history_dir, exist_ok=True)
    
    history_file = os.path.join(history_dir, f'{app_type}_history.json')
    
    history_entries = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history_entries = json.load(f)
        except (json.JSONDecodeError, IOError):
            history_entries = []
    
    new_entry = {
        'id': entry_data['id'],
        'name': entry_data['name'],
        'operation_type': entry_data['operation_type'],
        'instance_name': entry_data['instance_name'],
        'timestamp': datetime.now().isoformat(),
        'app_type': app_type
    }
    
    history_entries.append(new_entry)
    
    try:
        with open(history_file, 'w') as f:
            json.dump(history_entries, f, indent=2)
        return new_entry
    except IOError:
        return None