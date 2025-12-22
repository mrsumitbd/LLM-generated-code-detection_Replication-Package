import torch
from typing import NamedTuple, List, Optional

class DecodingResult(NamedTuple):
    """Simple result container for decoding."""
    text: str
    tokens: torch.Tensor
    probs: Optional[List[float]] = None

def decode_with_fallback(segment: torch.Tensor) -> DecodingResult:
    """
    Attempt to decode a tensor of token ids into a string. If decoding fails,
    fall back to an empty string while preserving the original tokens.

    Parameters
    ----------
    segment : torch.Tensor
        1‑D tensor containing integer token ids.

    Returns
    -------
    DecodingResult
        Named tuple containing the decoded text, the original tokens,
        and optionally a list of probabilities (None if not available).
    """
    # Ensure the tensor is on CPU and is a 1‑D sequence of ints
    try:
        # Convert to a Python list of ints
        token_ids = segment.cpu().tolist()
        # Basic ASCII decoding: map each id to a printable character
        # If an id is outside the printable ASCII range, skip it.
        decoded_chars = [
            chr(t) for t in token_ids
            if isinstance(t, int) and 32 <= t <= 126
        ]
        decoded_text = ''.join(decoded_chars)
        return DecodingResult(text=decoded_text, tokens=segment)
    except Exception:
        # Fallback: return an empty string but keep the original tokens
        return DecodingResult(text='', tokens=segment)