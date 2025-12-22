import csv
from pathlib import Path

def append_dict_to_csv(file_path: Path, data: dict):
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)