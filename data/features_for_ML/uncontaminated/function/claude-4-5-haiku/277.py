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
    chunks = []
    
    # Add content block stop event
    chunks.append((
        "content_block_stop",
        {"type": "content_block_stop", "index": 0}
    ))
    
    # Create message delta with stop reason
    message_delta = {
        "type": "message_delta",
        "delta": {"stop_reason": stop_reason}
    }
    if stop_sequence is not None:
        message_delta["delta"]["stop_sequence"] = stop_sequence
    
    chunks.append(("message_delta", message_delta))
    
    # Add message stop event
    chunks.append((
        "message_stop",
        {"type": "message_stop"}
    ))
    
    return chunks