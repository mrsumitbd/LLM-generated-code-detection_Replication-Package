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
        required_columns = ["timestamp", "value"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"CSV file must contain a '{col}' column.")
        return df
    except Exception as e:
        raise ValueError(f"Error loading and validating data: {e}") from e