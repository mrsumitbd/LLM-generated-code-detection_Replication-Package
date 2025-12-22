def create_tmp_json(data_dict, json_path):
    import json
    import tempfile
    import os
    
    # Create a temporary file in the same directory as json_path to ensure same filesystem
    temp_dir = os.path.dirname(json_path) or '.'
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False, suffix='.json') as tmp_file:
        json.dump(data_dict, tmp_file, ensure_ascii=False, indent=2)
        tmp_path = tmp_file.name
    
    return tmp_path