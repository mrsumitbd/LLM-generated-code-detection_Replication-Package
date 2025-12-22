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
    if not csv_file.exists():
        raise ValueError(f"CSV file not found: {csv_file}")
    
    if not csv_file.is_file():
        raise ValueError(f"Path is not a file: {csv_file}")
    
    if csv_file.suffix.lower() != '.csv':
        raise ValueError(f"File is not a CSV file: {csv_file}")
    
    try:
        df = pl.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")
    
    if df.is_empty():
        raise ValueError("CSV file is empty")
    
    if len(df.columns) == 0:
        raise ValueError("CSV file has no columns")
    
    return df