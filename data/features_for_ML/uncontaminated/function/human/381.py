from pathlib import Path
from datetime import datetime
import hashlib
from typing import Dict, Any, List, Optional
from agentic.utils.fingerprint import generate_fingerprint
from agentic.utils.file_reader import get_last_path_component, read_file

def prepare_document_metadata(
    file_path: str,
    text: str,
    mime_type: str,
    model: str
) -> Dict[str, Any]:
    """Prepare document metadata including fingerprint and summary"""
    is_url = file_path.startswith(("http://", "https://"))
    fingerprint = generate_fingerprint(text)
    
    metadata = {
        "filename": Path(file_path).name if not is_url else get_last_path_component(file_path),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mime_type": mime_type,
        "source_url": file_path if is_url else str(Path(file_path).absolute()),
        "fingerprint": fingerprint
    }
    
    # Generate document ID from filename
    metadata["document_id"] = hashlib.sha256(
        metadata["filename"].encode()
    ).hexdigest()
    
    return metadata