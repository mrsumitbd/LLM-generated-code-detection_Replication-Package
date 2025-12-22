from pathlib import Path
import polars as pl

def load_and_validate_data(csv_file: Path) -> pl.DataFrame:
    """
    Load CSV data and validate its structure.

    Args:
        csv_file: Path to the CSV file

    Returns:
        Polars DataFrame with the benchmark data

    Raises:
        ValueError: If the CSV structure is invalid
    """
    try:
        df = pl.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

    required_columns = ["tool", "method", "execution_time_seconds", "memory_mb"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return df