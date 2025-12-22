from pydantic import BaseModel, ValidationError
from lettucedetect_api.models import DetectionRequest, SpanDetectionResponse, TokenDetectionResponse

def _create_request_safe(contexts: list[str], question: str, answer: str) -> DetectionRequest:
    try:
        return DetectionRequest(contexts=contexts, question=question, answer=answer)
    except ValidationError as e:
        raise InvalidRequestError from e