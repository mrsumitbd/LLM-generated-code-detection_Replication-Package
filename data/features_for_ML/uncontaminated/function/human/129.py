from openevals.types import (
    EvaluatorResult,
    SimpleEvaluator,
    SimpleAsyncEvaluator,
    ModelClient,
    ChatCompletionMessage,
    FewShotExample,
    ScoreType,
)

def _append_few_shot_examples(
    *,
    messages: list[ChatCompletionMessage],
    few_shot_examples: list[FewShotExample],
) -> list[ChatCompletionMessage]:
    # Find the last user message to append examples to
    last_user_message_idx = None
    for i, msg in enumerate(messages[::-1]):
        if msg.get("role") == "user":
            last_user_message_idx = len(messages) - 1 - i
            break

    if last_user_message_idx is None:
        raise ValueError(
            "Appending few-shot examples requires a user message in the provided prompt"
        )

    messages[last_user_message_idx]["content"] += "\n\n" + "\n".join(  # type: ignore
        [
            f"<example>\n<input>{example['inputs']}</input>\n<output>{example['outputs']}</output>"
            + (
                f"\n<reasoning>{example['reasoning']}</reasoning>"
                if "reasoning" in example
                else ""
            )
            + (f"\n<score>{example['score']}</score>" if "score" in example else "")
            + "\n</example>"
            for example in few_shot_examples
        ]
    )
    return messages