def create_streaming_end_chunks(
    stop_reason: str = "end_turn", stop_sequence: str | None = None
) -> list[tuple[str, dict[str, Any]]]:
    """
    Create the final streaming chunks for Anthropic API format.

    Args:
        stop_reason: The reason for stopping
        stop_sequence: The stop sequence used (if any)

    Returns:
        List of tuples (event_type, chunk) for final streaming chunks
    """
    end_chunk = {
        "type": "result",
        "stop_reason": stop_reason,
        "stop_sequence": stop_sequence,
    }
    return [("result", end_chunk)]