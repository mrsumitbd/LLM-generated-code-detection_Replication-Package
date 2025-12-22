def _format_index(index: sqlalchemy.engine.interfaces.ReflectedIndex) -> str:
    """Format a reflected index into a string representation."""
    name = index.get('name', '')
    columns = index.get('column_names', [])
    unique = index.get('unique', False)
    
    columns_str = ', '.join(columns)
    unique_str = 'UNIQUE ' if unique else ''
    
    return f"{unique_str}INDEX {name} ({columns_str})"