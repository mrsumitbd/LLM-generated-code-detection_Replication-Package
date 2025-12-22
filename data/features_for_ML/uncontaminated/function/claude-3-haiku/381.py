import hashlib
import re
from typing import Dict, Any
from transformers import pipeline

def prepare_document_metadata(
    file_path: str,
    text: str,
    mime_type: str,
    model: str
) -> Dict[str, Any]:
    """Prepare document metadata including fingerprint and summary"""
    fingerprint = hashlib.sha256(text.encode()).hexdigest()
    summarizer = pipeline("summarization", model=model)
    summary = summarizer(text, max_length=100, min_length=20, do_sample=False)[0]["summary_text"]
    metadata = {
        "file_path": file_path,
        "mime_type": mime_type,
        "fingerprint": fingerprint,
        "summary": summary
    }
    return metadata