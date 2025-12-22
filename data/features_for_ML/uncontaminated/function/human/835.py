import os

def get_dir_of_file(file_path):
    if file_path:
        return os.path.dirname(file_path)
    return os.path.curdir