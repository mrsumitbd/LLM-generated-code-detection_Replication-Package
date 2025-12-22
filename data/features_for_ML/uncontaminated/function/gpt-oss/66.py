import base64
import json
from typing import Dict, Optional

import requests


def _get_file_content(
    file_path: str,
    headers: Dict[str, str],
    org: str,
    repo: str = "build-your-own-x",
    ref: str = "master",
) -> Optional[str]:
    """
    Get the content of a file from the repository.

    Parameters
    ----------
    file_path : str
        Path to the file inside the repository.
    headers : Dict[str, str]
        HTTP headers to send with the request (e.g. authentication).
    org : str
        GitHub organization or user name.
    repo : str, default "build-your-own-x"
        Repository name.
    ref : str, default "master"
        Git reference (branch, tag, or commit SHA).

    Returns
    -------
    Optional[str]
        The decoded file content as a string, or None if the file could not be retrieved.
    """
    # Build the GitHub API URL for the file contents endpoint
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{file_path}"
    params = {"ref": ref}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException:
        return None

    # If the file is not found or another error occurs, return None
    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    # The GitHub API returns the file content base64-encoded in the "content" field
    content_b64 = data.get("content")
    if content_b64 is None:
        return None

    # The content may contain newlines; remove them before decoding
    content_b64 = content_b64.replace("\n", "")

    try:
        decoded_bytes = base64.b64decode(content_b64)
    except (base64.binascii.Error, ValueError):
        return None

    try:
        return decoded_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # If the file is binary, return None
        return None