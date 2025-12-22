def get_chained_entity_path(entity_name: str) -> str:
    entity_parts = entity_name.split('.')
    chained_path = ''
    for i, part in enumerate(entity_parts):
        chained_path += f'["{part}"]'
        if i < len(entity_parts) - 1:
            chained_path += '.'
    return chained_path