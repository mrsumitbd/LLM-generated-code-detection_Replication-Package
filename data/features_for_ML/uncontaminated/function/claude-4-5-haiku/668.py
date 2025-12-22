def run_roomie_diagnostics(old, new):
    # Do not run diagnostics in edit mode
    if old is None:
        return
    
    # Check if roomie configuration has changed
    if old == new:
        return
    
    # Validate new configuration
    if new is None:
        return
    
    # Check for required fields
    required_fields = ['name', 'room_id']
    for field in required_fields:
        if field not in new:
            raise ValueError(f"Missing required field: {field}")
    
    # Check for valid room_id
    if not isinstance(new.get('room_id'), (int, str)):
        raise TypeError("room_id must be an integer or string")
    
    # Check for valid name
    if not isinstance(new.get('name'), str) or not new.get('name').strip():
        raise ValueError("name must be a non-empty string")
    
    # Check for configuration conflicts
    if 'max_occupancy' in new and 'min_occupancy' in new:
        if new['max_occupancy'] < new['min_occupancy']:
            raise ValueError("max_occupancy cannot be less than min_occupancy")
    
    # Validate numeric fields
    numeric_fields = ['max_occupancy', 'min_occupancy', 'temperature']
    for field in numeric_fields:
        if field in new and not isinstance(new[field], (int, float)):
            raise TypeError(f"{field} must be numeric")
    
    return True