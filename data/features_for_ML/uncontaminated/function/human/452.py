from src.primary.utils.database import get_manager_database
from src.primary.notification_manager import send_history_notification

def add_history_entry(app_type, entry_data):
    """
    Add a history entry for processed media
    
    Parameters:
    - app_type: str - The app type (sonarr, radarr, etc)
    - entry_data: dict - Entry data containing id, name, operation_type, instance_name
    
    Returns:
    - dict - The created history entry or None if failed
    """
    if app_type not in history_locks:
        logger.error(f"Invalid app type: {app_type}")
        return None
    
    # Extract instance name from entry data
    instance_name = entry_data.get("instance_name", "Default")
    
    logger.debug(f"Adding history entry for {app_type} with instance_name: '{instance_name}'")
    
    # Thread-safe database operation
    with history_locks[app_type]:
        try:
            manager_db = get_manager_database()
            entry = manager_db.add_hunt_history_entry(
                app_type=app_type,
                instance_name=instance_name,
                media_id=entry_data["id"],
                processed_info=entry_data["name"],
                operation_type=entry_data.get("operation_type", "missing"),
                discovered=False  # Default to false - will be updated by discovery tracker
            )
            
            # Add additional fields for compatibility
            entry["app_type"] = app_type  # Include app_type in the entry for display in UI
            
            logger.info(f"Added history entry for {app_type}-{instance_name}: {entry_data['name']}")
            
            # Send notification about this history entry
            try:
                # Import here to avoid circular imports
                from src.primary.notification_manager import send_history_notification
                send_history_notification(entry)
            except Exception as e:
                logger.error(f"Failed to send notification for history entry: {e}")
            
            return entry
            
        except Exception as e:
            logger.error(f"Database error adding history entry for {app_type}: {e}")
            return None