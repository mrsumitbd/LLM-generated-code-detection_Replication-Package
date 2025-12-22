import pandas as pd

def _load_data(dataset_name: str, backend: str) -> pd.DataFrame:
    """
    Load one of the available datasets in fleur.

    Args:
        dataset_name: A string specifying the name of the dataset. Currently,
            "iris", "mtcars" and "titanic" are supported.
        backend: The output format of the dataframe.

    Returns:
        A dataframe with the specified dataset.
    """
    datasets = {
        "iris": pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/master/pandas/tests/data/iris.csv"),
        "mtcars": pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/master/pandas/tests/data/mtcars.csv"),
        "titanic": pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/master/pandas/tests/data/titanic.csv")
    }

    if dataset_name not in datasets:
        raise ValueError(f"Dataset '{dataset_name}' is not supported.")

    df = datasets[dataset_name]

    if backend == "pandas":
        return df
    elif backend == "polars":
        import polars as pl
        return pl.from_pandas(df)
    elif backend == "duckdb":
        import duckdb
        return duckdb.from_pandas(df)
    else:
        raise ValueError(f"Backend '{backend}' is not supported.")