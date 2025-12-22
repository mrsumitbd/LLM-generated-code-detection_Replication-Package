import csv
import os

def get_voltages(shotn):
    """
    Retrieve voltage measurements for a given shot number.

    The function looks for a CSV file named `voltages_<shotn>.csv` in the current
    working directory. The CSV is expected to have a header row and a column
    named `voltage`. All voltage values are returned as a list of floats.
    If the file does not exist or cannot be read, an empty list is returned.
    """
    filename = f"voltages_{shotn}.csv"
    voltages = []

    if not os.path.isfile(filename):
        return voltages

    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    voltages.append(float(row["voltage"]))
                except (KeyError, ValueError):
                    # Skip rows that don't have a valid voltage entry
                    continue
    except Exception:
        # In case of any I/O or parsing error, return what we have so far
        pass

    return voltages