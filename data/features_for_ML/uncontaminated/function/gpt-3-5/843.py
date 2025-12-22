import json
import tempfile
import os

def create_tmp_json(data_dict, json_path):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        json.dump(data_dict, tmp_file)
        tmp_file_path = tmp_file.name

    os.replace(tmp_file_path, json_path)