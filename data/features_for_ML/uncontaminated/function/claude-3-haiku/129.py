def _append_few_shot_examples(
    *,
    messages: list[ChatCompletionMessage],
    few_shot_examples: list[FewShotExample],
) -> list[ChatCompletionMessage]:
    # Find the last user message to append examples to
    for i, message in reversed(list(enumerate(messages))):
        if message.role == "user":
            break
    else:
        return messages

    for example in few_shot_examples:
        messages.insert(i + 1, example.to_chat_completion_message())

    return messages