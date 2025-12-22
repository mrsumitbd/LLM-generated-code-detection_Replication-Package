import json
import tempfile
import os

def create_tmp_json(data_dict, json_path):
    """
    Create a temporary JSON file containing the provided data_dict.
    The temporary file will be created in the same directory as json_path
    to ensure it is on the same filesystem (useful for atomic moves).
    Returns the path to the temporary file.
    """
    # Ensure the directory exists
    dir_name = os.path.dirname(os.path.abspath(json_path))
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    # Create a named temporary file in the target directory
    tmp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        prefix='tmp_',
        dir=dir_name,
        delete=False,
        encoding='utf-8'
    )
    try:
        json.dump(data_dict, tmp_file, ensure_ascii=False, indent=4)
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
    finally:
        tmp_file.close()

    return tmp_file.name