import os
import json
import pandas as pd
from typing import Union

def get_predictions_from_file(predictions_path: str, dataset_name: str, split: str) -> pd.DataFrame:
    """
    Load predictions from a file or directory and return a pandas DataFrame filtered by
    `dataset_name` and `split`.

    Parameters
    ----------
    predictions_path : str
        Path to a file or directory containing prediction data. If a directory,
        the function will look for a file matching the pattern
        `{dataset_name}_{split}.csv` or `{dataset_name}_{split}.json`. If a file,
        it will be read directly.
    dataset_name : str
        Name of the dataset to filter on (if the file contains multiple datasets).
    split : str
        Split name to filter on (e.g., 'train', 'valid', 'test').

    Returns
    -------
    pd.DataFrame
        DataFrame containing the predictions, optionally filtered by dataset_name
        and split. If the file does not contain these columns, the entire DataFrame
        is returned.

    Raises
    ------
    FileNotFoundError
        If the specified file or matching file in a directory cannot be found.
    ValueError
        If the file format is unsupported or the file cannot be parsed.
    """
    # Helper to read a file into a DataFrame
    def _read_file(file_path: str) -> pd.DataFrame:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".csv":
            return pd.read_csv(file_path)
        elif ext in {".json", ".jsonl"}:
            # Try to read as JSON lines first
            try:
                return pd.read_json(file_path, lines=True)
            except ValueError:
                # Fallback to standard JSON
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return pd.DataFrame(data)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    # If predictions_path is a directory, search for a matching file
    if os.path.isdir(predictions_path):
        # Build possible filenames
        candidates = [
            os.path.join(predictions_path, f"{dataset_name}_{split}.csv"),
            os.path.join(predictions_path, f"{dataset_name}_{split}.json"),
            os.path.join(predictions_path, f"{dataset_name}_{split}.jsonl"),
        ]
        # If no candidate exists, try a generic pattern
        if not any(os.path.exists(c) for c in candidates):
            # Search for any file containing both dataset_name and split in its name
            for fname in os.listdir(predictions_path):
                if dataset_name in fname and split in fname:
                    candidates.append(os.path.join(predictions_path, fname))
            if not any(os.path.exists(c) for c in candidates):
                raise FileNotFoundError(
                    f"No prediction file found for dataset '{dataset_name}' and split '{split}' "
                    f"in directory '{predictions_path}'."
                )
        # Pick the first existing candidate
        for cand in candidates:
            if os.path.exists(cand):
                file_path = cand
                break
    else:
        # predictions_path is a file
        if not os.path.exists(predictions_path):
            raise FileNotFoundError(f"Prediction file '{predictions_path}' does not exist.")
        file_path = predictions_path

    # Read the file into a DataFrame
    df = _read_file(file_path)

    # If the DataFrame contains dataset_name and split columns, filter
    if {"dataset_name", "split"}.issubset(df.columns):
        df = df[(df["dataset_name"] == dataset_name) & (df["split"] == split)].copy()
    elif {"dataset", "split"}.issubset(df.columns):
        df = df[(df["dataset"] == dataset_name) & (df["split"] == split)].copy()
    elif {"dataset_name"}.issubset(df.columns):
        df = df[df["dataset_name"] == dataset_name].copy()
    elif {"split"}.issubset(df.columns):
        df = df[df["split"] == split].copy()

    # Reset index for cleanliness
    df.reset_index(drop=True, inplace=True)
    return df