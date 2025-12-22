import csv
import os
from typing import Dict, Any

def run_analysis() -> Dict[str, Any]:
    """
    Reads a CSV file named 'data.csv' in the current working directory,
    computes the mean of each numeric column, prints the results,
    and returns a dictionary mapping column names to their mean values.
    If the file does not exist or contains no numeric data, an empty
    dictionary is returned.
    """
    filename = "data.csv"
    if not os.path.isfile(filename):
        return {}

    numeric_sums: Dict[str, float] = {}
    numeric_counts: Dict[str, int] = {}

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                try:
                    num = float(value)
                except (ValueError, TypeError):
                    continue
                numeric_sums[key] = numeric_sums.get(key, 0.0) + num
                numeric_counts[key] = numeric_counts.get(key, 0) + 1

    means: Dict[str, float] = {}
    for key in numeric_sums:
        count = numeric_counts[key]
        if count > 0:
            means[key] = numeric_sums[key] / count

    # Print the results
    if means:
        print("Mean values for numeric columns:")
        for col, mean_val in means.items():
            print(f"  {col}: {mean_val}")
    else:
        print("No numeric data found in 'data.csv'.")

    return means