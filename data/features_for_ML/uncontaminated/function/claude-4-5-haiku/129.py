def _append_few_shot_examples(
    *,
    messages: list[ChatCompletionMessage],
    few_shot_examples: list[FewShotExample],
) -> list[ChatCompletionMessage]:
    if not few_shot_examples or not messages:
        return messages
    
    # Create a copy to avoid modifying the original list
    result = messages.copy()
    
    # Find the last user message
    last_user_index = -1
    for i in range(len(result) - 1, -1, -1):
        if result[i].get("role") == "user":
            last_user_index = i
            break
    
    # If no user message found, return original messages
    if last_user_index == -1:
        return result
    
    # Build the few-shot examples content
    examples_content = ""
    for example in few_shot_examples:
        examples_content += f"Input: {example.get('input', '')}\n"
        examples_content += f"Output: {example.get('output', '')}\n\n"
    
    # Append examples to the last user message
    last_user_message = result[last_user_index]
    current_content = last_user_message.get("content", "")
    
    if isinstance(current_content, str):
        last_user_message["content"] = current_content + "\n\n" + examples_content.strip()
    elif isinstance(current_content, list):
        # If content is a list of content blocks, append as text
        last_user_message["content"].append({
            "type": "text",
            "text": "\n\n" + examples_content.strip()
        })
    
    return result