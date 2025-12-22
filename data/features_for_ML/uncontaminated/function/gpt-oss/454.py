import csv
import json
import os
from pathlib import Path

def convert(path: str) -> None:
    """
    Convert a CSV file to a JSON file.

    The function reads the CSV file located at `path`, converts its contents
    into a list of dictionaries (one per row), and writes the result to a
    new file with the same base name but a `.json` extension in the same
    directory. Existing output files are overwritten.

    Parameters
    ----------
    path : str
        Path to the input CSV file.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If the input file is not a CSV file (does not end with .csv).
    """
    # Validate input file
    input_path = Path(path)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")

    if input_path.suffix.lower() != ".csv":
        raise ValueError(f"Input file must be a CSV: {path}")

    # Read CSV data
    with input_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Prepare output path
    output_path = input_path.with_suffix(".json")

    # Write JSON data
    with output_path.open("w", encoding="utf-8") as jsonfile:
        json.dump(rows, jsonfile, ensure_ascii=False, indent=4)