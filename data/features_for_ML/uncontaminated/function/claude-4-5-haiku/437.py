def write_to_container(container: Container, data: str, dst: Path):
    """
    Write a string to a file in a docker container
    """
    import io
    
    # Convert data to bytes
    data_bytes = data.encode('utf-8')
    
    # Create a file-like object
    file_obj = io.BytesIO(data_bytes)
    
    # Put the file into the container
    container.put_archive(str(dst.parent), file_obj)