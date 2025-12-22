import logging
from pathlib import Path, PurePosixPath
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload

def upload_file(
    service,
    target_filename: str,
    content_type: str,
    coords,
    filename=None,
    file_stream=None,
) -> None:
    """Upload a file to Google Drive; auto-create subfolders from target_filename."""

    # Check that "coords.path_id" is a folder
    meta = (
        service.files()
        .get(
            fileId=coords.path_id,
            fields="id, mimeType",
            supportsAllDrives=True,
        )
        .execute()
    )
    if meta.get("mimeType") != "application/vnd.google-apps.folder":
        raise ValueError(f"path_id must be a folder, got {meta.get('mimeType')}")

    # If "target_filename" contains subfolders, create them and find the deepest folder id.
    target_path = PurePosixPath(target_filename)
    if str(target_path.parent) and str(target_path.parent) != ".":
        parent_id = _create_subfolders(service, coords.path_id, str(target_path.parent))
    else:
        parent_id = coords.path_id

    # Upload file
    chunk_size = 8 * 1024 * 1024
    if file_stream is not None:
        media = MediaIoBaseUpload(
            file_stream, mimetype=content_type, chunksize=chunk_size, resumable=True
        )
    else:
        media = MediaFileUpload(
            filename, mimetype=content_type, chunksize=chunk_size, resumable=True
        )
    request = service.files().create(
        body={"name": target_path.name, "parents": [parent_id]},
        media_body=media,
        fields="id, name, webViewLink",
        supportsAllDrives=True,
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            prog = getattr(status, "resumable_progress", None)
            if prog is not None:
                logging.info("uploading %s: %d bytes sent", filename, prog)
            else:
                logging.info("uploading %s...", filename)

    logging.info(
        "uploaded %s (%s) → %s",
        response.get("name"),
        response.get("id"),
        response.get("webViewLink"),
    )