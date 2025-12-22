import os
from typing import Any, Iterable, Optional

from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from googleapiclient.errors import HttpError


def _get_folder_id(service, folder_name: str, parent_id: Optional[str]) -> str:
    """
    Return the ID of a folder with the given name under the specified parent.
    If it does not exist, create it.
    """
    query = (
        f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' "
        f"and trashed = false"
    )
    if parent_id:
        query += f" and '{parent_id}' in parents"
    else:
        query += " and 'root' in parents"

    try:
        results = (
            service.files()
            .list(q=query, spaces="drive", fields="nextPageToken, files(id, name)")
            .execute()
        )
    except HttpError as e:
        raise RuntimeError(f"Error listing folders: {e}") from e

    files = results.get("files", [])
    if files:
        return files[0]["id"]

    # Folder does not exist; create it
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        folder_metadata["parents"] = [parent_id]

    try:
        folder = (
            service.files()
            .create(body=folder_metadata, fields="id")
            .execute()
        )
    except HttpError as e:
        raise RuntimeError(f"Error creating folder '{folder_name}': {e}") from e

    return folder["id"]


def _ensure_path(service, path_parts: Iterable[str]) -> str:
    """
    Ensure that the folder path exists and return the ID of the deepest folder.
    """
    parent_id = None
    for part in path_parts:
        parent_id = _get_folder_id(service, part, parent_id)
    return parent_id


def upload_file(
    service,
    target_filename: str,
    content_type: str,
    coords: Any,
    filename: Optional[str] = None,
    file_stream: Optional[Any] = None,
) -> None:
    """
    Upload a file to Google Drive; auto-create subfolders from target_filename.

    Parameters
    ----------
    service : googleapiclient.discovery.Resource
        Authenticated Drive API service instance.
    target_filename : str
        Full path including folders and file name, e.g. "folder1/folder2/file.txt".
    content_type : str
        MIME type of the file to upload.
    coords : Any
        Unused parameter kept for API compatibility.
    filename : str, optional
        Path to a local file to upload. Ignored if ``file_stream`` is provided.
    file_stream : file-like object, optional
        Stream containing the file data. If provided, ``filename`` is ignored.

    Returns
    -------
    None
    """
    # Split the target path into folder parts and the final file name
    parts = target_filename.strip("/").split("/")
    if not parts:
        raise ValueError("target_filename must contain at least a file name")

    *folder_parts, final_name = parts

    # Ensure the folder hierarchy exists
    parent_id = _ensure_path(service, folder_parts) if folder_parts else None

    # Prepare the file metadata
    file_metadata = {"name": final_name}
    if parent_id:
        file_metadata["parents"] = [parent_id]

    # Determine the media body
    if file_stream is not None:
        media = MediaIoBaseUpload(file_stream, mimetype=content_type, resumable=True)
    elif filename is not None:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        media = MediaFileUpload(filename, mimetype=content_type, resumable=True)
    else:
        raise ValueError("Either filename or file_stream must be provided")

    # Upload the file
    try:
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    except HttpError as e:
        raise RuntimeError(f"Error uploading file '{final_name}': {e}") from e