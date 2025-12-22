import anthropic
import base64
import mimetypes
from pathlib import Path
from typing import Literal


def extract_simple(
    file_path: str,
    mime_type: str | None = None,
    response_format: Literal["text", "markdown"] = "text",
) -> str:
    """
    Extract text content from a file using Claude's vision capabilities.
    
    Args:
        file_path: Path to the file to extract text from
        mime_type: MIME type of the file (auto-detected if None)
        response_format: Format of the response ("text" or "markdown")
    
    Returns:
        Extracted text content from the file
    """
    # Read the file and encode it as base64
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine MIME type
    if mime_type is None:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            # Default to application/octet-stream if we can't determine the type
            mime_type = "application/octet-stream"
    
    # Read and encode the file
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    file_base64 = base64.standard_b64encode(file_data).decode("utf-8")
    
    # Create Anthropic client
    client = anthropic.Anthropic()
    
    # Prepare the prompt based on response format
    if response_format == "markdown":
        prompt = "Please extract all text content from this file and format it as markdown. Preserve the structure and formatting as much as possible."
    else:
        prompt = "Please extract all text content from this file."
    
    # Call Claude API with vision
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": file_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    
    # Extract and return the text content
    return message.content[0].text