from pathlib import Path
import csv

def append_dict_to_csv(file_path: Path, data: dict):
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(data)