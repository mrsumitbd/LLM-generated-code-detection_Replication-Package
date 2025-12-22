def upload_file(
    service,
    target_filename: str,
    content_type: str,
    coords,
    filename=None,
    file_stream=None,
) -> None:
    """Upload a file to Google Drive; auto-create subfolders from target_filename."""
    from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload

    # Split the target_filename into directory and file name
    file_parts = target_filename.split('/')
    file_name = file_parts.pop()
    parent_folders = '/'.join(file_parts)

    # Create the parent folders if they don't exist
    current_folder = ''
    for folder in file_parts:
        current_folder += f'{folder}/'
        try:
            folder_metadata = {'name': folder, 'mimeType': 'application/vnd.google-apps.folder'}
            folder = service.files().create(body=folder_metadata, fields='id').execute()
        except:
            pass

    # Prepare the file metadata
    file_metadata = {'name': file_name, 'parents': [current_folder]}
    if coords:
        file_metadata['imageMediaMetadata'] = {'location': coords}

    # Upload the file
    if filename:
        media = MediaFileUpload(filename, resumable=True)
    elif file_stream:
        media = MediaInMemoryUpload(file_stream.read(), resumable=True)
    else:
        raise ValueError('Either filename or file_stream must be provided.')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()