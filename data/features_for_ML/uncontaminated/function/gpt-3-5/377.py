def _load_data(dataset_name: str, backend: str) -> Frame:
    if dataset_name == "iris":
        if backend == "pandas":
            return pd.DataFrame(data=datasets.load_iris().data, columns=datasets.load_iris().feature_names)
        elif backend == "dask":
            return dd.from_pandas(pd.DataFrame(data=datasets.load_iris().data, columns=datasets.load_iris().feature_names), npartitions=2)
    elif dataset_name == "mtcars":
        if backend == "pandas":
            return pd.DataFrame(data=datasets.load_mtcars().data, columns=datasets.load_mtcars().feature_names)
        elif backend == "dask":
            return dd.from_pandas(pd.DataFrame(data=datasets.load_mtcars().data, columns=datasets.load_mtcars().feature_names), npartitions=2)
    elif dataset_name == "titanic":
        if backend == "pandas":
            return pd.DataFrame(data=datasets.load_titanic().data, columns=datasets.load_titanic().feature_names)
        elif backend == "dask":
            return dd.from_pandas(pd.DataFrame(data=datasets.load_titanic().data, columns=datasets.load_titanic().feature_names), npartitions=2)