def get_spark_pool_id(container: VirtualItemContainer, name) -> str:
    for item in container.items:
        if isinstance(item, SparkPool) and item.name == name:
            return item.id
    return ""