import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload


def upload_file(
    service,
    target_filename: str,
    content_type: str,
    coords,
    filename=None,
    file_stream=None,
) -> None:
    """Upload a file to Google Drive; auto-create subfolders from target_filename."""
    
    # Parse the target_filename to extract folder path and file name
    parts = target_filename.split('/')
    file_name = parts[-1]
    folder_path = parts[:-1]
    
    # Start from the root folder (coords should contain the root folder ID)
    current_folder_id = coords
    
    # Create folders as needed
    for folder_name in folder_path:
        if folder_name:  # Skip empty strings
            # Check if folder already exists
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{current_folder_id}' in parents and trashed=false"
            results = service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=10).execute()
            items = results.get('files', [])
            
            if items:
                # Folder exists, use its ID
                current_folder_id = items[0]['id']
            else:
                # Create new folder
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [current_folder_id]
                }
                folder = service.files().create(body=file_metadata, fields='id').execute()
                current_folder_id = folder.get('id')
    
    # Prepare file metadata
    file_metadata = {
        'name': file_name,
        'parents': [current_folder_id]
    }
    
    # Prepare media upload
    if file_stream is not None:
        # If file_stream is provided, use it
        if isinstance(file_stream, str):
            # If it's a string, treat it as file content
            media = MediaIoBaseUpload(io.BytesIO(file_stream.encode()), mimetype=content_type)
        else:
            # If it's a file-like object
            media = MediaIoBaseUpload(file_stream, mimetype=content_type)
    elif filename is not None:
        # If filename is provided, read from file
        media = MediaFileUpload(filename, mimetype=content_type)
    else:
        # No file content provided
        raise ValueError("Either filename or file_stream must be provided")
    
    # Upload the file
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()