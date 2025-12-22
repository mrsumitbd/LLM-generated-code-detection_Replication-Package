import os

def get_dir_of_file(file_path):
    """
    Return the directory component of the given file path.
    
    Parameters
    ----------
    file_path : str
        The path to a file. Can be relative or absolute.
    
    Returns
    -------
    str
        The directory part of the path. If the input is None or an empty string,
        an empty string is returned.
    """
    if not file_path:
        return ""
    return os.path.dirname(file_path)