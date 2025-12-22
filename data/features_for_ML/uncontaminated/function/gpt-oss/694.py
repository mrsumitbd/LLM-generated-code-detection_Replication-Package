import os
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The bucket name should be set in an environment variable.
# If not set, the function will raise a ValueError.
BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")


def delete_file_from_s3(object_key: str) -> None:
    """
    Delete an object from an S3 bucket.

    Parameters
    ----------
    object_key : str
        The key (path) of the object to delete.

    Raises
    ------
    ValueError
        If the bucket name is not configured.
    """
    if not BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME environment variable is not set")

    s3_client = boto3.client("s3")

    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_key)
        logger.info("Deleted %s from bucket %s", object_key, BUCKET_NAME)
    except ClientError as exc:
        logger.error(
            "Failed to delete %s from bucket %s: %s",
            object_key,
            BUCKET_NAME,
            exc,
        )
        raise