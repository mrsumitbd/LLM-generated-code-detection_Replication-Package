import narwhals.stable.v2 as nw
import os
from narwhals.stable.v2.typing import Frame

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
    dataset_name: str = dataset_name.lower()

    if dataset_name not in AVAILABLE_DATASETS:
        raise ValueError(
            f"dataset_name must be one of: {' ,'.join(AVAILABLE_DATASETS)}"
        )

    dataset_file: str = f"{dataset_name}.csv"
    dataset_path: str = os.path.join(PACKAGE_DIR, dataset_file)
    df: Frame = nw.read_csv(dataset_path, backend=backend)

    return df.to_native()