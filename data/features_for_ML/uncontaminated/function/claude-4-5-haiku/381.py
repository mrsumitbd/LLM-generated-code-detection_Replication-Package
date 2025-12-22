import hashlib
import json
from typing import Any, Dict
import anthropic


def prepare_document_metadata(
    file_path: str,
    text: str,
    mime_type: str,
    model: str
) -> Dict[str, Any]:
    """Prepare document metadata including fingerprint and summary"""
    
    # Generate fingerprint using SHA-256 hash of the text content
    fingerprint = hashlib.sha256(text.encode()).hexdigest()
    
    # Create the client
    client = anthropic.Anthropic()
    
    # Generate summary using Claude API
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please provide a brief summary (2-3 sentences) of the following document:\n\n{text[:2000]}"
            }
        ]
    )
    
    summary = message.content[0].text
    
    # Prepare metadata dictionary
    metadata = {
        "file_path": file_path,
        "mime_type": mime_type,
        "fingerprint": fingerprint,
        "summary": summary,
        "text_length": len(text),
        "model_used": model
    }
    
    return metadata