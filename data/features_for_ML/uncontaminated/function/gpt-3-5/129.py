def _append_few_shot_examples(
    *,
    messages: list[ChatCompletionMessage],
    few_shot_examples: list[FewShotExample],
) -> list[ChatCompletionMessage]:
    if not messages:
        return messages
    
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].sender == Sender.USER:
            messages[i].few_shot_examples.extend(few_shot_examples)
            break
    
    return messages