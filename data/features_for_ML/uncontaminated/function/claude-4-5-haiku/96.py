def html_escape(s):
    """Escape HTML special characters in a string."""
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;'
    }
    
    result = s
    for char, escape_seq in replacements.items():
        result = result.replace(char, escape_seq)
    
    return result