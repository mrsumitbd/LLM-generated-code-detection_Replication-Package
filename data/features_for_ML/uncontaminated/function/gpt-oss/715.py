from typing import List, Optional
from botocore.paginate import Paginator

def get_source_files(
    s3_source_client,
    s3_source_resource,
    s3_coords,
) -> List[str]:
    """
    Return a list of S3 object keys that match the given coordinates.

    Parameters
    ----------
    s3_source_client : botocore.client.BaseClient
        The low‑level S3 client used for pagination.
    s3_source_resource : boto3.resources.base.ServiceResource
        The high‑level S3 resource (unused in this implementation but kept for API compatibility).
    s3_coords : object
        An object that must expose at least the following attributes:
            - bucket_name (str)
            - prefix (str, optional)
            - suffix (str, optional)

    Returns
    -------
    List[str]
        A list of object keys that exist in the bucket under the given prefix
        and that optionally match the suffix filter.
    """
    # Extract coordinates with defaults
    bucket_name: str = getattr(s3_coords, "bucket_name", None)
    if not bucket_name:
        raise ValueError("s3_coords must provide a 'bucket_name' attribute")

    prefix: str = getattr(s3_coords, "prefix", "")
    suffix: Optional[str] = getattr(s3_coords, "suffix", None)

    # Use paginator to handle large result sets
    paginator: Paginator = s3_source_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    keys: List[str] = []

    for page in page_iterator:
        contents = page.get("Contents", [])
        for obj in contents:
            key: str = obj["Key"]
            if suffix is None or key.endswith(suffix):
                keys.append(key)

    return keys