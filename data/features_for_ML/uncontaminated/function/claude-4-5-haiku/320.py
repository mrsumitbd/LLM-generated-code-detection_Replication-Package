import csv
from pathlib import Path

def append_dict_to_csv(file_path: Path, data: dict):
    """Append a dictionary as a row to a CSV file."""
    file_exists = file_path.exists()
    
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)