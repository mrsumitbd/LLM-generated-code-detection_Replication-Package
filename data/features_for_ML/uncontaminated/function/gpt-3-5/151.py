def format_file_size(bytes_size):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes_size) < 1024.0:
            return "%3.1f %sB" % (bytes_size, unit)
        bytes_size /= 1024.0
    return "%.1f %sB" % (bytes_size, 'Y')