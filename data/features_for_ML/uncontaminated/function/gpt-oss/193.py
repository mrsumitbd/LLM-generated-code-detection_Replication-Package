def extract_and_store_features(dataset, model, repo):
    """
    Extract features from each item in `dataset` using `model` and store them in `repo`.

    Parameters
    ----------
    dataset : Iterable
        An iterable of data items. Each item may be a dict, an object with an `id` attribute,
        or any type accepted by `model`.
    model : Callable
        A callable that accepts a single data item and returns its feature representation.
    repo : Any
        An object that provides a method to store features. The method name is detected
        automatically: it looks for `save`, `add`, `store`, or `write`. The method must
        accept two positional arguments: a key (identifier) and the feature data.

    Returns
    -------
    dict
        A mapping from item keys to the extracted features. This dictionary is also
        stored in `repo` via the detected method.
    """
    # Determine the storage method name
    storage_method_name = None
    for name in ("save", "add", "store", "write"):
        if hasattr(repo, name) and callable(getattr(repo, name)):
            storage_method_name = name
            break
    if storage_method_name is None:
        raise AttributeError(
            "The repository object does not provide a suitable storage method "
            "(expected one of: save, add, store, write)."
        )
    storage_method = getattr(repo, storage_method_name)

    # Prepare the result dictionary
    extracted = {}

    # Iterate over the dataset
    for idx, item in enumerate(dataset):
        # Extract features
        try:
            features = model(item)
        except Exception:
            # Skip items that raise errors during feature extraction
            continue

        # Determine a key for the item
        key = None
        if hasattr(item, "id"):
            key = getattr(item, "id")
        elif isinstance(item, dict) and "id" in item:
            key = item["id"]
        else:
            key = idx

        # Store the features in the repository
        try:
            storage_method(key, features)
        except Exception:
            # If storage fails, skip this item but keep the feature in the result dict
            pass

        # Record the extracted features
        extracted[key] = features

    return extracted