from __future__ import annotations

from typing import List

# Try to import the real DetectionRequest if it exists.
try:
    from .detection_request import DetectionRequest  # type: ignore
except Exception:  # pragma: no cover
    # Fallback definition for environments where the real class is not available.
    from dataclasses import dataclass

    @dataclass
    class DetectionRequest:
        contexts: List[str]
        question: str
        answer: str


def _create_request_safe(contexts: list[str], question: str, answer: str) -> DetectionRequest:
    """
    Safely construct a DetectionRequest object from the provided inputs.

    Parameters
    ----------
    contexts : list[str]
        A list of context strings. If None or not a list, it will be converted to an empty list.
    question : str
        The question string. If None, it will be converted to an empty string.
    answer : str
        The answer string. If None, it will be converted to an empty string.

    Returns
    -------
    DetectionRequest
        A new DetectionRequest instance with sanitized inputs.
    """
    # Ensure contexts is a list of strings
    if contexts is None:
        safe_contexts: List[str] = []
    else:
        try:
            # If contexts is not a list, try to iterate over it
            safe_contexts = [str(c) for c in contexts]
        except TypeError:
            # If contexts is a single string, wrap it in a list
            safe_contexts = [str(contexts)]

    # Ensure question and answer are strings
    safe_question = str(question) if question is not None else ""
    safe_answer = str(answer) if answer is not None else ""

    return DetectionRequest(
        contexts=safe_contexts,
        question=safe_question,
        answer=safe_answer,
    )