import logging
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.service_resource import S3ServiceResource
from docling_jobkit.datamodel.s3_coords import S3Coordinates

def get_source_files(
    s3_source_client: S3Client,
    s3_source_resource: S3ServiceResource,
    s3_coords: S3Coordinates,
):
    source_paginator = s3_source_client.get_paginator("list_objects_v2")

    key_prefix = (
        s3_coords.key_prefix
        if s3_coords.key_prefix.endswith("/")
        else s3_coords.key_prefix + "/"
    )
    if key_prefix == "/":
        key_prefix = ""
    # Check that source is not empty
    source_count = count_s3_objects(source_paginator, s3_coords.bucket, key_prefix)
    if source_count == 0:
        logging.error("No documents to process in the source s3 coordinates.")
    return get_keys_s3_objects_as_set(s3_source_resource, s3_coords.bucket, key_prefix)