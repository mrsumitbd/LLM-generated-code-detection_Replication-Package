import os
import shutil

def convert(path: str) -> None:
    """
    Converts the file or directory at the given path to a different format.
    
    Args:
        path (str): The path to the file or directory to be converted.
    """
    if os.path.isfile(path):
        # Convert a single file
        base, ext = os.path.splitext(path)
        new_path = f"{base}.new{ext}"
        shutil.copy(path, new_path)
        print(f"Converted file: {path} -> {new_path}")
    elif os.path.isdir(path):
        # Convert all files in a directory
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(file_path)
                new_path = os.path.join(dirpath, f"{base}.new{ext}")
                shutil.copy(file_path, new_path)
                print(f"Converted file: {file_path} -> {new_path}")
    else:
        print(f"Error: {path} is not a valid file or directory.")