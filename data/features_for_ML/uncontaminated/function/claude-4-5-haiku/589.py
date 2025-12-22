def _get_spark_pool_id(container: VirtualItemContainer, spark_pool_name: str) -> str:
    """Get the Spark pool ID from the container by name."""
    for item in container.items:
        if hasattr(item, 'name') and item.name == spark_pool_name:
            if hasattr(item, 'id'):
                return item.id
    raise ValueError(f"Spark pool '{spark_pool_name}' not found in container")