from typing import Any

def create_streaming_end_chunks(
        stop_reason: str = "end_turn", stop_sequence: str | None = None
    ) -> list[tuple[str, dict[str, Any]]]:
    
    chunks = []
    
    if stop_sequence is not None:
        chunks.append(("stop_sequence", {"stop_sequence": stop_sequence}))
    
    chunks.append(("stop_reason", {"stop_reason": stop_reason}))
    
    return chunks