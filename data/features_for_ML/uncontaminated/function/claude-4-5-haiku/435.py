def _create_request_safe(contexts: list[str], question: str, answer: str) -> DetectionRequest:
    return DetectionRequest(
        contexts=contexts,
        question=question,
        answer=answer
    )