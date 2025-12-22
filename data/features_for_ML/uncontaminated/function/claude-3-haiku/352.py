import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class PromptData:
    prompt: str
    response: str
    metadata: dict

def _parse_jsonl_line(
    line: str, line_num: int, task_logger=None
) -> Optional[PromptData]:
    try:
        data = json.loads(line)
        if not isinstance(data, dict) or 'prompt' not in data or 'response' not in data:
            if task_logger:
                task_logger.error(f"Invalid JSONL line {line_num}: {line}")
            return None
        return PromptData(
            prompt=data['prompt'],
            response=data['response'],
            metadata=data.get('metadata', {})
        )
    except (ValueError, KeyError) as e:
        if task_logger:
            task_logger.error(f"Error parsing JSONL line {line_num}: {line}")
            task_logger.exception(e)
        return None