def get_source_files(
    s3_source_client: S3Client,
    s3_source_resource: S3ServiceResource,
    s3_coords: S3Coordinates,
):
    """
    Retrieves a list of source files from an S3 bucket.

    Args:
        s3_source_client (S3Client): An S3 client instance.
        s3_source_resource (S3ServiceResource): An S3 service resource instance.
        s3_coords (S3Coordinates): An object containing the S3 bucket and prefix information.

    Returns:
        List[str]: A list of source file names.
    """
    source_files = []

    try:
        bucket = s3_source_resource.Bucket(s3_coords.bucket)
        objects = bucket.objects.filter(Prefix=s3_coords.prefix)

        for obj in objects:
            source_files.append(obj.key)

    except Exception as e:
        print(f"Error retrieving source files: {e}")

    return source_files