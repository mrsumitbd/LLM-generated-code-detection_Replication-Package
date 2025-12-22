from typing import Dict, Any

def prepare_document_metadata(
    file_path: str,
    text: str,
    mime_type: str,
    model: str
) -> Dict[str, Any]:
    metadata = {
        'file_path': file_path,
        'text': text,
        'mime_type': mime_type,
        'model': model,
        'fingerprint': hash(text),
        'summary': text[:100] + '...' if len(text) > 100 else text
    }
    return metadata