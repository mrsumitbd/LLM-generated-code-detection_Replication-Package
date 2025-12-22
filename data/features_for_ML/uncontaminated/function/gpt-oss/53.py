from typing import Callable
from pyspark.sql import SparkSession
import uuid

def get_isolation_provider() -> Callable:
    """
    Get the isolation provider for the current Spark session.

    Returns:
        Callable: A function that returns isolation context as a string.
    """
    # Obtain the active Spark session or create one if none exists
    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    # Define the provider function that returns a string representing the isolation context
    def provider() -> str:
        # Try to fetch a session‑specific identifier from Spark configuration.
        # If none is set, fall back to a newly generated UUID.
        return spark.conf.get("spark.sql.session.id", str(uuid.uuid4()))

    return provider