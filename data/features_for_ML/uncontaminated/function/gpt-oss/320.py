from pathlib import Path
import csv

def append_dict_to_csv(file_path: Path, data: dict):
    """
    Append a dictionary as a row to a CSV file. If the file does not exist,
    it will be created with a header derived from the dictionary keys.
    If the file exists, the row will be appended using the existing header order.
    """
    # Ensure the parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine if the file exists
    file_exists = file_path.is_file()

    if not file_exists:
        # Create file with header from data keys
        with file_path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(data.keys()))
            writer.writeheader()
            writer.writerow(data)
    else:
        # Read existing header to preserve column order
        with file_path.open('r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                # Empty file: treat as no header
                header = []

        # If header is empty, use data keys
        if not header:
            header = list(data.keys())

        # Append the row
        with file_path.open('a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerow(data)