import pandas as pd
from typing import Union

# Optional imports for other backends
try:
    import polars as pl
except ImportError:
    pl = None

try:
    import seaborn as sns
except ImportError:
    sns = None

try:
    import statsmodels.api as sm
except ImportError:
    sm = None


def _load_data(dataset_name: str, backend: str) -> Union[pd.DataFrame, "pl.DataFrame"]:
    """
    Load one of the available datasets in fleur.

    Args:
        dataset_name: A string specifying the name of the dataset. Currently,
            "iris", "mtcars" and "titanic" are supported.
        backend: The output format of the dataframe.

    Returns:
        A dataframe with the specified dataset.
    """
    # Validate dataset name
    name = dataset_name.lower()
    if name not in {"iris", "mtcars", "titanic"}:
        raise ValueError(f"Unsupported dataset '{dataset_name}'. "
                         f"Supported datasets: iris, mtcars, titanic.")

    # Load data into a pandas DataFrame
    if name == "iris":
        if sns is None:
            raise ImportError("seaborn is required to load the iris dataset.")
        df = sns.load_dataset("iris")
    elif name == "titanic":
        if sns is None:
            raise ImportError("seaborn is required to load the titanic dataset.")
        df = sns.load_dataset("titanic")
    elif name == "mtcars":
        if sm is None:
            raise ImportError("statsmodels is required to load the mtcars dataset.")
        mtcars = sm.datasets.get_rdataset("mtcars")
        df = mtcars.data
    else:
        # This branch is unreachable due to earlier validation
        raise ValueError(f"Unhandled dataset '{dataset_name}'.")

    # Convert to requested backend
    backend = backend.lower()
    if backend == "pandas":
        return df
    elif backend == "polars":
        if pl is None:
            raise ImportError("polars is required for the 'polars' backend.")
        return pl.DataFrame(df)
    else:
        raise ValueError(f"Unsupported backend '{backend}'. "
                         f"Supported backends: pandas, polars.")