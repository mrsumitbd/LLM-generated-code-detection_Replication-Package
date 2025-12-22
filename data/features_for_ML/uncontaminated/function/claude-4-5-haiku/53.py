def get_isolation_provider() -> Callable:
    """ Get the isolation provider for the current Spark session.

        Returns:
            Callable: A function that returns isolation context as a string.
    """
    from pyspark.sql import SparkSession
    
    def isolation_provider() -> str:
        spark = SparkSession.getActiveSession()
        if spark is None:
            return "SERIALIZABLE"
        
        conf = spark.sparkContext.getConf()
        isolation_level = conf.get("spark.sql.shuffle.partitions", None)
        
        # Check for isolation level configuration
        isolation = conf.get("spark.sql.isolationLevel", "SERIALIZABLE")
        return isolation
    
    return isolation_provider