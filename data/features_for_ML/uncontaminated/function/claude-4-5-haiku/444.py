def check_optimizer_groups(optimizer_groups):
    """
    Check if optimizer_groups is a valid list of optimizer parameter groups.
    
    Returns True if valid, False otherwise.
    """
    if not isinstance(optimizer_groups, list):
        return False
    
    if len(optimizer_groups) == 0:
        return False
    
    for group in optimizer_groups:
        if not isinstance(group, dict):
            return False
        
        if 'params' not in group:
            return False
        
        if not isinstance(group['params'], (list, tuple)):
            return False
        
        if len(group['params']) == 0:
            return False
    
    return True