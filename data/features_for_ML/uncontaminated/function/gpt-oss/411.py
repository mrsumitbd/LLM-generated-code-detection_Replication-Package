import os

def create_text_entry(name: str):
    """
    Create an empty text file with the given name (appending .txt if not present)
    and return the absolute path to the created file.
    """
    # Ensure the filename ends with .txt
    if not name.lower().endswith('.txt'):
        filename = f"{name}.txt"
    else:
        filename = name

    # Create or truncate the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("")  # create an empty file

    # Return the absolute path
    return os.path.abspath(filename)