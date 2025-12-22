import boto3

def delete_file_from_s3(object_key) -> None:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('your_bucket_name')
    bucket.delete_objects(Delete={'Objects': [{'Key': object_key}]})