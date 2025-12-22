from typing import Any, List, Tuple

def create_streaming_end_chunks(
    stop_reason: str = "end_turn",
    stop_sequence: str | None = None,
) -> List[Tuple[str, dict[str, Any]]]:
    """
    Create the final streaming chunks for Anthropic API format.

    Args:
        stop_reason: The reason for stopping.
        stop_sequence: The stop sequence used (if any).

    Returns:
        List of tuples (event_type, chunk) for final streaming chunks.
    """
    # Build the content block stop chunk
    content_block_stop: dict[str, Any] = {"stop_reason": stop_reason}
    if stop_sequence is not None:
        content_block_stop["stop_sequence"] = stop_sequence

    # Build the message stop chunk
    message_stop: dict[str, Any] = {"stop_reason": stop_reason}
    if stop_sequence is not None:
        message_stop["stop_sequence"] = stop_sequence

    return [
        ("content_block_stop", content_block_stop),
        ("message_stop", message_stop),
    ]