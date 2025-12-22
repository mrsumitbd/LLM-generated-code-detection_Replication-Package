from typing import List
from pydantic import BaseModel

class DetectionRequest(BaseModel):
    contexts: List[str]
    question: str
    answer: str

def _create_request_safe(contexts: List[str], question: str, answer: str) -> DetectionRequest:
    return DetectionRequest(
        contexts=contexts,
        question=question,
        answer=answer
    )