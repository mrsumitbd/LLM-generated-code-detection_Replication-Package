def upload_file(service, target_filename: str, content_type: str, coords, filename=None, file_stream=None) -> None:
    folder_id = 'root'
    for folder_name in target_filename.split('/')[:-1]:
        folder_id = create_folder(service, folder_name, folder_id)
    file_metadata = {
        'name': target_filename.split('/')[-1],
        'parents': [folder_id]
    }
    media = MediaFileUpload(filename, mimetype=content_type)
    service.files().create(body=file_metadata, media_body=media).execute()

def create_folder(service, folder_name, parent_id):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')