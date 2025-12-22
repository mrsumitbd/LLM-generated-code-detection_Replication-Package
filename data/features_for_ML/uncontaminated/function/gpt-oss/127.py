import pandas as pd

def prep(df):
    """
    Basic preprocessing of a pandas DataFrame:
    - Drop rows containing any missing values.
    - Convert boolean columns to integers.
    - Attempt to convert object columns to numeric types when possible.
    """
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Drop rows with any missing values
    df = df.dropna()

    # Convert boolean columns to integers
    bool_cols = df.select_dtypes(include=['bool']).columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(int)

    # Attempt to convert object columns to numeric
    obj_cols = df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception:
            # If conversion fails, leave the column as is
            pass

    return df