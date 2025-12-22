def _get_spark_pool_id(container: VirtualItemContainer, spark_pool_name: str) -> str:
    """
    Retrieve the ID of a Spark pool by name from a VirtualItemContainer.

    Parameters
    ----------
    container : VirtualItemContainer
        The container that holds Spark pool resources.
    spark_pool_name : str
        The name of the Spark pool to look up.

    Returns
    -------
    str
        The ID of the requested Spark pool.

    Raises
    ------
    ValueError
        If the Spark pool cannot be found.
    """
    # Prefer a direct lookup if the container exposes a get_spark_pool method
    if hasattr(container, "get_spark_pool"):
        try:
            pool = container.get_spark_pool(spark_pool_name)
            return pool.id
        except Exception:
            pass  # fall back to enumeration

    # Fallback: enumerate all Spark pools and match by name
    if hasattr(container, "list_spark_pools"):
        for pool in container.list_spark_pools():
            if getattr(pool, "name", None) == spark_pool_name:
                return getattr(pool, "id", None)

    # If we reach here, the pool was not found
    raise ValueError(f"Spark pool '{spark_pool_name}' not found in the provided container.")