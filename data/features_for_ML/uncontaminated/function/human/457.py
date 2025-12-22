from typing import Any, Literal
from kreuzberg.extraction import (
    batch_extract_bytes_sync,
    batch_extract_file_sync,
    extract_bytes_sync,
    extract_file_sync,
)

def extract_simple(
    file_path: str,
    mime_type: str | None = None,
    response_format: Literal["text", "markdown"] = "text",
) -> str:
    validated_path = _validate_file_path(file_path)
    config = _create_config_with_overrides()
    result = extract_file_sync(str(validated_path), mime_type, config)
    if response_format == "markdown":
        return result.to_markdown(show_metadata=False)
    return result.content