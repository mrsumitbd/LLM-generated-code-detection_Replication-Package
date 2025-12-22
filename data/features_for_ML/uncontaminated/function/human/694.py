import boto3
from syftr.configuration import REPO_ROOT, S3_TIMEOUT, cfg
from syftr.utils.locks import distributed_lock

def delete_file_from_s3(object_key) -> None:
    s3 = boto3.client("s3")

    with distributed_lock(
        f"{cfg.storage.cache_bucket}/{object_key}", timeout_s=S3_TIMEOUT
    ):
        if check_file_exists_s3(object_key):
            s3.delete_object(Bucket=cfg.storage.cache_bucket, Key=object_key)