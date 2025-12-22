from typing import List
import boto3
from botocore.client import BaseClient

def get_source_files(
    s3_source_client: BaseClient,
    s3_source_resource: boto3.resources.base.ServiceResource,
    s3_coords: List[str],
):
    bucket = s3_coords[0]
    prefix = s3_coords[1]
    
    s3_bucket = s3_source_resource.Bucket(bucket)
    objects = s3_bucket.objects.filter(Prefix=prefix)
    
    files = []
    for obj in objects:
        files.append(obj.key)
    
    return files