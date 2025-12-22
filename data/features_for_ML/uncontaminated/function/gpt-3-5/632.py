def get_chained_entity_path(entity_name: str) -> str:
    if entity_name == 'user':
        return 'user -> profile -> account'
    elif entity_name == 'product':
        return 'product -> details -> reviews'
    elif entity_name == 'order':
        return 'order -> items -> payment'
    else:
        return 'Unknown entity'