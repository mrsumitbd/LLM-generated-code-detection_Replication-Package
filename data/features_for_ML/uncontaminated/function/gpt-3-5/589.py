def _get_spark_pool_id(container: VirtualItemContainer, spark_pool_name: str) -> str:
    for item in container.virtual_items:
        if isinstance(item, SparkPool) and item.name == spark_pool_name:
            return item.id
    return ""