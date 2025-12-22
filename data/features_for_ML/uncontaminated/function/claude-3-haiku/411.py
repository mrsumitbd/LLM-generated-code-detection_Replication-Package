def create_text_entry(name: str):
    """
    Creates a new text entry with the given name.

    Args:
        name (str): The name of the text entry.

    Returns:
        dict: A dictionary representing the new text entry, with the following keys:
            - 'name': the name of the text entry
            - 'content': an empty string
            - 'created_at': the current timestamp
            - 'updated_at': the current timestamp
    """
    import datetime

    text_entry = {
        'name': name,
        'content': '',
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now()
    }

    return text_entry