import csv
from pathlib import Path
from filelock import FileLock
from syftr.logger import logger

def append_dict_to_csv(file_path: Path, data: dict):
    file_path = Path(file_path).resolve()
    lock = FileLock(file_path.with_suffix(".lock"))
    with lock:
        logger.info("Appending data to file: %s", file_path)
        file_exists = file_path.exists()
        with file_path.open(mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)