def get_source_files(
    s3_source_client: S3Client,
    s3_source_resource: S3ServiceResource,
    s3_coords: S3Coordinates,
):
    bucket = s3_coords.bucket
    prefix = s3_coords.prefix
    
    source_files = []
    
    try:
        paginator = s3_source_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        
        for page in pages:
            if 'Contents' not in page:
                continue
            
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('/'):
                    continue
                
                s3_object = s3_source_resource.Object(bucket, key)
                source_files.append(s3_object)
        
        return source_files
    
    except Exception as e:
        raise Exception(f"Error retrieving source files from S3: {str(e)}")