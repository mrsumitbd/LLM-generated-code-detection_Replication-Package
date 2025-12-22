def get_spark_pool_id(container: VirtualItemContainer, name) -> str:
    for item in container.items:
        if hasattr(item, 'name') and item.name == name:
            if hasattr(item, 'id'):
                return item.id
    return ""