def _get_spark_pool_id(container: VirtualItemContainer, spark_pool_name: str) -> str:
    spark_pools = container.get_spark_pools()
    for spark_pool in spark_pools:
        if spark_pool.name == spark_pool_name:
            return spark_pool.id
    raise ValueError(f"Spark pool '{spark_pool_name}' not found in the container.")