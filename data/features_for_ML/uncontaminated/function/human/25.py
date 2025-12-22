from local_operator.types import ActionType, CodeExecutionResult

def _parse_action_content(content: str, result: CodeExecutionResult, partial: bool = False) -> None:
    """
    Parses the content within action_response tags and populates the result object.

    Args:
        content (str): The content between <action_response> and </action_response> tags.
        result (CodeExecutionResult): The result object to populate.
        partial (bool): Whether this is a partial parse (incomplete action_response).

    Raises:
        ValueError: If an invalid ActionType is encountered.
    """
    tags = [
        "action",
        "content",
        "code",
        "replacements",
        "mentioned_files",
        "learnings",
        "file_path",
        "agent",
    ]

    for tag in tags:
        open_tag = f"<{tag}>"
        close_tag = f"</{tag}>"

        start_idx = 0
        while True:
            open_idx = content.find(open_tag, start_idx)
            if open_idx == -1:
                break

            close_idx = content.find(close_tag, open_idx)
            if close_idx == -1:
                # If we're doing partial parsing and there's no closing tag,
                # extract the content after the opening tag
                if partial:
                    partial_content = content[open_idx + len(open_tag) :]
                    if tag == "mentioned_files":
                        _handle_partial_mentioned_files(partial_content, result)
                    else:
                        # For other tags, assign the partial content directly
                        _assign_tag_content(tag, partial_content, result, partial=True)
                break

            tag_content = content[open_idx + len(open_tag) : close_idx]
            _assign_tag_content(tag, tag_content, result, partial=False)

            start_idx = close_idx + len(close_tag)