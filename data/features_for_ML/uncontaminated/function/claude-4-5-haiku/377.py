def _load_data(dataset_name: str, backend: str) -> Frame:
    """
    Load one of the available datasets in fleur.

    Args:
        dataset_name: A string specifying the name of the dataset. Currently,
            "iris", "mtcars" and "titanic" are supported.
        backend: The output format of the dataframe.

    Returns:
        A dataframe with the specified dataset.
    """
    import pandas as pd
    from pathlib import Path
    
    # Map dataset names to their file paths
    datasets = {
        "iris": "iris.csv",
        "mtcars": "mtcars.csv",
        "titanic": "titanic.csv"
    }
    
    if dataset_name not in datasets:
        raise ValueError(f"Dataset '{dataset_name}' not found. Available datasets: {list(datasets.keys())}")
    
    # Get the directory where this module is located
    module_dir = Path(__file__).parent
    data_dir = module_dir / "data"
    file_path = data_dir / datasets[dataset_name]
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Convert to the specified backend format
    if backend == "pandas":
        return df
    elif backend == "polars":
        try:
            import polars as pl
            return pl.from_pandas(df)
        except ImportError:
            raise ImportError("Polars is not installed. Please install it to use the 'polars' backend.")
    elif backend == "pyarrow":
        try:
            import pyarrow as pa
            return pa.Table.from_pandas(df)
        except ImportError:
            raise ImportError("PyArrow is not installed. Please install it to use the 'pyarrow' backend.")
    else:
        raise ValueError(f"Backend '{backend}' not supported. Available backends: 'pandas', 'polars', 'pyarrow'")