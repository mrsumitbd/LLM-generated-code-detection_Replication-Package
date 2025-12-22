def get_spark_pool_id(container: VirtualItemContainer, name) -> str:
    for item in container.items:
        if item.name == name and isinstance(item, SparkPool):
            return item.id
    return ""