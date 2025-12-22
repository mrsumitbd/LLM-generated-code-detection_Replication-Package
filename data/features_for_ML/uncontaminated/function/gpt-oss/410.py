import os
import csv
from pathlib import Path
from typing import List, Optional

from . import defs
from .document import Document


def load_csv_dir(
    dir_path: str,
    encoding: str = defs.FILE_ENCODING,
    text_tag: str = defs.TEXT_COLUMN,
    metadata_tags: Optional[List[str]] = None,
    max_text_length: Optional[int] = None,
) -> List[Document]:
    """
    Load a directory of CSV files and return a list of Document objects.

    Parameters
    ----------
    dir_path : str
        Path to the directory containing CSV files.
    encoding : str, optional
        File encoding to use when reading CSV files. Defaults to defs.FILE_ENCODING.
    text_tag : str, optional
        Column name that contains the text content for each document. Defaults to defs.TEXT_COLUMN.
    metadata_tags : list[str] | None, optional
        List of column names to include as metadata. If None, all columns except `text_tag` are used.
    max_text_length : int | None, optional
        Maximum length of the text content. If provided, text will be truncated to this length.

    Returns
    -------
    list[Document]
        A list of Document objects created from the CSV files.
    """
    documents: List[Document] = []

    # Resolve directory path
    dir_path_obj = Path(dir_path).expanduser().resolve()
    if not dir_path_obj.is_dir():
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    # Find all CSV files in the directory (non-recursive)
    csv_files = list(dir_path_obj.glob("*.csv"))
    if not csv_files:
        return documents  # return empty list if no CSV files found

    for csv_file in csv_files:
        try:
            with csv_file.open(mode="r", encoding=encoding, newline="") as f:
                reader = csv.DictReader(f)
                # Determine which metadata columns to use
                if metadata_tags is None:
                    # Use all columns except the text_tag
                    meta_keys = [k for k in reader.fieldnames if k != text_tag]
                else:
                    meta_keys = [k for k in metadata_tags if k in reader.fieldnames]

                for row in reader:
                    # Skip rows that don't have the required text_tag
                    if text_tag not in row or row[text_tag] is None:
                        continue

                    text = row[text_tag]
                    if max_text_length is not None:
                        text = text[:max_text_length]

                    # Build metadata dictionary
                    metadata = {k: row[k] for k in meta_keys if k in row}

                    # Optionally add the source file name as metadata
                    metadata.setdefault("source", str(csv_file))

                    documents.append(Document(content=text, metadata=metadata))
        except Exception as exc:
            # Log the error and continue with next file
            # (Assuming a logger is available; otherwise, re-raise)
            raise RuntimeError(f"Error processing file {csv_file}: {exc}") from exc

    return documents