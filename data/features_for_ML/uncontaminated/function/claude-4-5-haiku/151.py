def format_file_size(bytes_size):
    """Format bytes into human-readable file size."""
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"