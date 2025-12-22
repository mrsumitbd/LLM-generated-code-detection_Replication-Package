import os

def write(filename: str, content: str):
    """
    Write the given content to the specified file.

    Parameters
    ----------
    filename : str
        Path to the file to write.
    content : str
        Text content to write into the file.

    Notes
    -----
    - The function will create any missing intermediate directories.
    - Existing files will be overwritten.
    - UTF-8 encoding is used for writing.
    """
    # Ensure the directory exists
    dir_name = os.path.dirname(os.path.abspath(filename))
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    # Write content to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)