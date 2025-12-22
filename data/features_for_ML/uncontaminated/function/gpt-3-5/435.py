def _create_request_safe(contexts: list[str], question: str, answer: str) -> DetectionRequest:
    request = DetectionRequest()
    request.contexts = contexts
    request.question = question
    request.answer = answer
    return request