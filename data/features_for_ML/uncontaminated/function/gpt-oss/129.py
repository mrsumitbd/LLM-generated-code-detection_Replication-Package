from __future__ import annotations

def _append_few_shot_examples(
    *,
    messages: list[ChatCompletionMessage],
    few_shot_examples: list[FewShotExample],
) -> list[ChatCompletionMessage]:
    """
    Append few‑shot examples to the last user message in a chat completion.

    Parameters
    ----------
    messages : list[ChatCompletionMessage]
        The original list of chat messages.
    few_shot_examples : list[FewShotExample]
        A list of examples to append.  Each example is expected to expose
        ``prompt`` and ``response`` attributes.

    Returns
    -------
    list[ChatCompletionMessage]
        A new list of messages with the examples appended to the last user
        message.  If no user message is found, the original list is returned.
    """
    # Find the index of the last user message
    last_user_index: int | None = None
    for idx in range(len(messages) - 1, -1, -1):
        msg = messages[idx]
        # Support both dict‑like and dataclass objects
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
        if role == "user":
            last_user_index = idx
            break

    # If there is no user message, return the original list unchanged
    if last_user_index is None:
        return messages

    # Build the examples string
    example_parts: list[str] = []
    for ex in few_shot_examples:
        # Support both dict‑like and dataclass objects for the example
        prompt = ex.get("prompt") if isinstance(ex, dict) else getattr(ex, "prompt", "")
        response = ex.get("response") if isinstance(ex, dict) else getattr(ex, "response", "")
        example_parts.append(f"User: {prompt}\nAssistant: {response}")

    examples_text = "\n\n".join(example_parts)

    # Append the examples to the content of the last user message
    last_msg = messages[last_user_index]
    content = last_msg.get("content") if isinstance(last_msg, dict) else getattr(last_msg, "content", "")
    new_content = f"{content}\n\n{examples_text}".strip()

    # Construct a new message preserving the original type
    if isinstance(last_msg, dict):
        new_msg = {**last_msg, "content": new_content}
    else:
        # Assume a dataclass or similar with a copy method
        new_msg = last_msg.__class__(**{**last_msg.__dict__, "content": new_content})

    # Build the new messages list
    new_messages = messages.copy()
    new_messages[last_user_index] = new_msg
    return new_messages