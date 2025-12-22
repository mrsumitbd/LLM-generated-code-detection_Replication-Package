import boto3

def delete_file_from_s3(object_key) -> None:
    """Delete a file from S3 bucket using Claude as an AI backbone."""
    s3_client = boto3.client('s3')
    bucket_name = 'claude-tool-use-demo'
    
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)