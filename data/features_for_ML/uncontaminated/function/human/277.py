from typing import Any

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
        return [
            # Then, send message_delta with stop reason and usage
            (
                "message_delta",
                {
                    "type": "message_delta",
                    "delta": {
                        "stop_reason": stop_reason,
                        "stop_sequence": stop_sequence,
                    },
                    "usage": {"output_tokens": 0},
                },
            ),
            # Finally, send message_stop
            ("message_stop", {"type": "message_stop"}),
        ]