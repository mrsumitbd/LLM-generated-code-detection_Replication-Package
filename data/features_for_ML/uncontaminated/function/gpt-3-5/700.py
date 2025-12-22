from pathlib import Path
import polars as pl

def load_and_validate_data(csv_file: Path) -> pl.DataFrame:
    df = pl.read_csv(csv_file)
    
    # Perform data validation here
    if not all(col in df.columns for col in ['column1', 'column2', 'column3']):
        raise ValueError("Invalid CSV structure. Missing required columns.")
    
    return df