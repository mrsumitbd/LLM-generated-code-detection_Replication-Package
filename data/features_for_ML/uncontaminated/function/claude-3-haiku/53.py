from typing import Callable
from pyspark.sql import SparkSession

def get_isolation_provider() -> Callable:
    """Get the isolation provider for the current Spark session.

    Returns:
        Callable: A function that returns isolation context as a string.
    """
    spark = SparkSession.getActiveSession()
    if spark is None:
        raise ValueError("No active Spark session found.")

    def get_isolation_context() -> str:
        return spark.conf.get("spark.sql.execution.isolationProvider", "NONE")

    return get_isolation_context