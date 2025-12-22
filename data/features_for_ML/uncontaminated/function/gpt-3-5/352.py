def _parse_jsonl_line(line: str, line_num: int, task_logger=None) -> Optional[PromptData]:
    try:
        data = json.loads(line)
        prompt_data = PromptData(data)
        return prompt_data
    except Exception as e:
        if task_logger:
            task_logger.error(f"Error parsing JSONL line {line_num}: {str(e)}")
        return None