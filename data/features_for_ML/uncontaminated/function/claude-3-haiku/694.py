import boto3

def delete_file_from_s3(object_key):
    """
    Deletes a file from an Amazon S3 bucket.

    Args:
        object_key (str): The key (filename) of the object to be deleted.

    Returns:
        None
    """
    s3 = boto3.client('s3')
    s3.delete_object(Bucket='your-bucket-name', Key=object_key)