import pandas as pd
from pathlib import Path

def load_study(study_name: str) -> pd.DataFrame:
    """
    Load a study dataset from the local `studies` directory.

    Parameters
    ----------
    study_name : str
        Name of the study file (without extension). The function will
        attempt to load a CSV or Parquet file with this name from the
        `studies` directory.

    Returns
    -------
    pd.DataFrame
        The loaded study data.

    Raises
    ------
    FileNotFoundError
        If no file matching the study name is found.
    """
    base_dir = Path(__file__).parent / "studies"
    # Try CSV first
    csv_path = base_dir / f"{study_name}.csv"
    if csv_path.is_file():
        return pd.read_csv(csv_path)

    # Try Parquet
    parquet_path = base_dir / f"{study_name}.parquet"
    if parquet_path.is_file():
        return pd.read_parquet(parquet_path)

    # If neither file exists, raise an error
    raise FileNotFoundError(
        f"Study '{study_name}' not found as CSV or Parquet in {base_dir}"
    )