import json
from typing import Any, Dict, List, Optional, Tuple, Union
from utils.logger import logger

def _parse_jsonl_line(
    line: str, line_num: int, task_logger=None
) -> Optional[PromptData]:
    """Parse a single JSONL line into PromptData.

    Args:
        line: The JSONL line to parse
        line_num: Line number for error reporting
        task_logger: Optional logger for this task

    Returns:
        PromptData object or None if parsing fails
    """
    effective_logger = task_logger if task_logger else logger

    try:
        json_obj = json.loads(line.strip())

        # Extract ID
        prompt_id = json_obj.get("id", line_num)

        # Extract and normalize prompt
        raw_prompt = json_obj.get("prompt")
        prompt = _normalize_prompt_field(raw_prompt)
        if not prompt:
            # For debugging, show the type and structure of the raw prompt
            prompt_info = f"type: {type(raw_prompt).__name__}"
            if isinstance(raw_prompt, dict) and "messages" in raw_prompt:
                prompt_info += f", has {len(raw_prompt['messages'])} messages"
            elif isinstance(raw_prompt, list):
                prompt_info += f", list length: {len(raw_prompt)}"
            effective_logger.warning(
                f"Empty prompt in line {line_num} ({prompt_info}): {line}..."
            )
            return None

        # Handle images
        image_base64 = ""
        image_url = ""

        # Process image_path for base64 encoding
        image_path = _normalize_image_path(json_obj.get("image_path"))
        if image_path:
            try:
                image_base64 = encode_image(image_path)
            except IOError as e:
                effective_logger.warning(f"Failed to encode image {image_path}: {e}")

        # Process image_url
        if "image_url" in json_obj:
            image_url_raw = json_obj["image_url"]
            if isinstance(image_url_raw, list) and image_url_raw:
                image_url = str(image_url_raw[0])
            elif isinstance(image_url_raw, str):
                image_url = image_url_raw

        return PromptData(prompt_id, prompt, image_base64, image_url)

    except json.JSONDecodeError as e:
        effective_logger.error(
            f"JSON decode error in line {line_num}: {line}. Error: {e}"
        )
        return None
    except Exception as e:
        effective_logger.error(f"Unexpected error parsing line {line_num}: {e}")
        return None