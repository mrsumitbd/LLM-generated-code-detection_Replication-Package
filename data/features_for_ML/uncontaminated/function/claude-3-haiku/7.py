import json
import os
from typing import Dict, List, Tuple

def generate_maestro_analysis_report(json_path: str):
    # Load embedded files
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Extract relevant information from the JSON data
    analysis_report = {
        'total_files': len(data['files']),
        'total_lines': sum(file['lines'] for file in data['files']),
        'total_functions': sum(len(file['functions']) for file in data['files']),
        'total_classes': sum(len(file['classes']) for file in data['files']),
        'file_stats': [],
        'function_stats': [],
        'class_stats': []
    }

    for file in data['files']:
        file_stats = {
            'name': file['name'],
            'lines': file['lines'],
            'functions': len(file['functions']),
            'classes': len(file['classes'])
        }
        analysis_report['file_stats'].append(file_stats)

        for function in file['functions']:
            function_stats = {
                'name': function['name'],
                'lines': function['lines'],
                'complexity': function['complexity']
            }
            analysis_report['function_stats'].append(function_stats)

        for class_info in file['classes']:
            class_stats = {
                'name': class_info['name'],
                'lines': class_info['lines'],
                'methods': len(class_info['methods'])
            }
            analysis_report['class_stats'].append(class_stats)

    return analysis_report