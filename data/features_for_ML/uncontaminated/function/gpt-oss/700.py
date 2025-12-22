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
    # Load the CSV file
    try:
        df = pl.read_csv(csv_file)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV file '{csv_file}': {exc}") from exc

    # Define required columns and their expected types
    required_columns = {
        "benchmark": pl.Utf8,
        "value": pl.Float64,
        "timestamp": pl.Datetime,
    }

    # Check that all required columns are present
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Validate column types
    for col, expected_type in required_columns.items():
        actual_type = df.schema[col]
        # Allow integer values for numeric columns
        if expected_type == pl.Float64 and actual_type in (pl.Int64, pl.Int32, pl.Int16, pl.Int8):
            # Cast to Float64
            df = df.with_columns(pl.col(col).cast(pl.Float64))
            actual_type = pl.Float64
        # For datetime, try to parse if not already datetime
        if expected_type == pl.Datetime and actual_type != pl.Datetime:
            try:
                df = df.with_columns(
                    pl.col(col).str.strptime(pl.Datetime, fmt="%Y-%m-%d %H:%M:%S")
                )
                actual_type = pl.Datetime
            except Exception:
                raise ValueError(
                    f"Column '{col}' cannot be parsed as datetime. "
                    f"Expected format 'YYYY-MM-DD HH:MM:SS'."
                )
        if actual_type != expected_type:
            raise ValueError(
                f"Column '{col}' has type {actual_type} but expected {expected_type}."
            )

    # Ensure no nulls in required columns
    null_counts = df.select(
        [(pl.col(col).null_count().alias(col)) for col in required_columns]
    ).to_dict(as_series=False)
    for col, count in null_counts.items():
        if count > 0:
            raise ValueError(f"Column '{col}' contains {count} null values.")

    return df