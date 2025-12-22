import csv
import json
import os
import sqlite3
from argparse import Namespace
from typing import Iterable, List, Tuple, Union


def _ensure_args(args: Namespace, *keys: str) -> None:
    """Raise a ValueError if any required key is missing."""
    missing = [k for k in keys if getattr(args, k, None) is None]
    if missing:
        raise ValueError(f"Missing required arguments: {', '.join(missing)}")


def _read_csv(file_path: str, delimiter: str = ",", header: bool = True) -> Tuple[List[str], List[Tuple]]:
    """Read a CSV file and return column names and data rows."""
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        return [], []

    if header:
        columns = rows[0]
        data_rows = [tuple(row) for row in rows[1:]]
    else:
        columns = [f"col{i + 1}" for i in range(len(rows[0]))]
        data_rows = [tuple(row) for row in rows]

    return columns, data_rows


def _read_json(file_path: str, header: bool = True) -> Tuple[List[str], List[Tuple]]:
    """Read a JSON file containing a list of objects and return column names and data rows."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of objects")

    if not data:
        return [], []

    if header:
        columns = list(data[0].keys())
        data_rows = [tuple(item.get(col, None) for col in columns) for item in data]
    else:
        columns = [f"col{i + 1}" for i in range(len(data[0]))]
        data_rows = [tuple(item.values()) for item in data]

    return columns, data_rows


def _create_table(cur: sqlite3.Cursor, table: str, columns: List[str]) -> None:
    """Create a table with the given columns if it does not exist."""
    col_defs = ", ".join([f"{col} TEXT" for col in columns])
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({col_defs})")


def _insert_rows(cur: sqlite3.Cursor, table: str, columns: List[str], rows: List[Tuple]) -> None:
    """Insert rows into the specified table."""
    placeholders = ", ".join(["?"] * len(columns))
    cur.executemany(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
        rows,
    )


def import_command(args: Namespace) -> None:
    """
    Import data from a CSV or JSON file into a SQLite database.

    Expected arguments in `args`:
        - file: Path to the input file (.csv or .json)
        - db: Path to the SQLite database file
        - table: Name of the table to import into
        - delimiter: (optional) CSV delimiter, defaults to ','
        - header: (optional) Whether the first row/keys are column names, defaults to True
    """
    _ensure_args(args, "file", "db", "table")

    file_path: str = args.file
    db_path: str = args.db
    table: str = args.table
    delimiter: str = getattr(args, "delimiter", ",")
    header: bool = getattr(args, "header", True)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.lower().endswith(".csv"):
        columns, data_rows = _read_csv(file_path, delimiter=delimiter, header=header)
    elif file_path.lower().endswith(".json"):
        columns, data_rows = _read_json(file_path, header=header)
    else:
        raise ValueError("Unsupported file format. Only .csv and .json are supported.")

    if not columns or not data_rows:
        print("No data to import.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    _create_table(cur, table, columns)
    _insert_rows(cur, table, columns, data_rows)

    conn.commit()
    conn.close()

    print(f"Imported {len(data_rows)} rows into table '{table}'.")