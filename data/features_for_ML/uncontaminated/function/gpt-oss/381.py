from typing import Dict, Any
import hashlib
import textwrap
import os

def prepare_document_metadata(
    file_path: str,
    text: str,
    mime_type: str,
    model: str
) -> Dict[str, Any]:
    """Prepare document metadata including fingerprint and summary"""

    # Compute a fingerprint (SHA-256) of the document text
    fingerprint = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Create a short summary: first 200 characters, trimmed to a word boundary
    summary = textwrap.shorten(text, width=200, placeholder="...")

    # Gather metadata
    metadata: Dict[str, Any] = {
        "file_path": file_path,
        "mime_type": mime_type,
        "model": model,
        "fingerprint": fingerprint,
        "summary": summary,
    }

    # Optionally include file size if the file exists
    try:
        if os.path.isfile(file_path):
            metadata["file_size_bytes"] = os.path.getsize(file_path)
    except Exception:
        pass

    return metadata