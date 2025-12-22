def apply_format(text, format_type):
    if format_type == 'uppercase':
        return text.upper()
    elif format_type == 'lowercase':
        return text.lower()
    elif format_type == 'titlecase':
        return text.title()
    else:
        return "Invalid format type"