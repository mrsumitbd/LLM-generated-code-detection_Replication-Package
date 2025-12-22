def get_spark_pool_id(container: VirtualItemContainer, name) -> str:
    """
    Retrieve the ID of a Spark pool from a VirtualItemContainer by its name.

    Parameters
    ----------
    container : VirtualItemContainer
        The container holding virtual items (e.g., Spark pools).
    name : str
        The name of the Spark pool to look up.

    Returns
    -------
    str
        The ID of the Spark pool.

    Raises
    ------
    ValueError
        If no Spark pool with the given name is found.
    """
    # Try the most common API first: get_item(name)
    try:
        item = container.get_item(name)
        # Some implementations expose the id via an `id` attribute
        if hasattr(item, "id"):
            return str(item.id)
        # Fallback: maybe the id is stored under a different attribute
        for attr in ("spark_pool_id", "pool_id", "resource_id"):
            if hasattr(item, attr):
                return str(getattr(item, attr))
    except Exception:
        # If get_item fails, fall back to iterating over items
        pass

    # Fallback: iterate over container.items or container.get_items()
    items = getattr(container, "items", None) or getattr(container, "get_items", lambda: [])()
    for item in items:
        if getattr(item, "name", None) == name:
            if hasattr(item, "id"):
                return str(item.id)
            for attr in ("spark_pool_id", "pool_id", "resource_id"):
                if hasattr(item, attr):
                    return str(getattr(item, attr))

    # If we reach here, the pool was not found
    raise ValueError(f"Spark pool with name '{name}' not found in the provided container.")