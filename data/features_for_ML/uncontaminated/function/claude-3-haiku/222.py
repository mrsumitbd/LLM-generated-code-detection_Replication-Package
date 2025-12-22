import os
import json

def convert_txt_to_json(txt_filepath: str, json_filepath: str, method: str, model: str, directory_path: str) -> None:
    """
    Convert analysis results from txt format to structured JSON format.
    
    Args:
        txt_filepath: Path to the input txt file
        json_filepath: Path to the output json file
        method: Analysis method used
        model: Model used for analysis
        directory_path: Input directory path
    """
    with open(txt_filepath, 'r') as txt_file:
        data = txt_file.read().splitlines()

    json_data = {
        'method': method,
        'model': model,
        'directory_path': directory_path,
        'results': []
    }

    for line in data:
        result = line.split('\t')
        json_data['results'].append({
            'item': result[0],
            'score': float(result[1])
        })

    with open(json_filepath, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)