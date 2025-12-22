import os
import json
import tempfile

def create_tmp_json(data_dict, json_path):
    # Create a temporary file to store the modified JSON data
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
        # Write the data_dict to the temporary file as JSON
        json.dump(data_dict, tmp_file)
        tmp_file_path = tmp_file.name

    # Move the temporary file to the specified json_path
    os.replace(tmp_file_path, json_path)