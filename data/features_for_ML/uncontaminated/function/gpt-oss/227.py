from typing import Optional, Union, Callable, Tuple

def handle_openai_compatible_response(
    model_provider: "ModelProvider",
    model_name: str,
    request: "FenicCompletionsRequest",
    response: Optional[Union["ChatCompletion", "ParsedChatCompletion"]],
    request_key_generator: Callable[["FenicCompletionsRequest"], str],
) -> Tuple[
        Optional[Union["ParsedChoice", "Choice"]],
        Optional[Union["FatalException", "TransientException"]]
    ]:
    """
    Handle a response that is compatible with the OpenAI API.

    The function attempts to extract the first choice from the response.
    If the response contains an error, a suitable exception is returned.
    """
    # Generate a request key for logging / caching purposes (unused here)
    _ = request_key_generator(request)

    # No response received
    if response is None:
        return None, TransientException("No response received from the model provider")

    # If the response is already parsed, just return the first choice
    if isinstance(response, ParsedChatCompletion):
        if not getattr(response, "choices", []):
            return None, TransientException("Parsed response contains no choices")
        return response.choices[0], None

    # Handle raw ChatCompletion responses
    if isinstance(response, ChatCompletion):
        # Check for an error field
        error = getattr(response, "error", None)
        if error is not None:
            # Determine if the error is fatal or transient
            err_type = getattr(error, "type", None)
            err_msg = getattr(error, "message", str(error))
            if err_type in ("invalid_request_error", "authentication_error", "rate_limit_error"):
                return None, FatalException(err_msg)
            return None, TransientException(err_msg)

        # Normal response: extract the first choice
        if not getattr(response, "choices", []):
            return None, TransientException("Response contains no choices")
        return response.choices[0], None

    # Unsupported response type
    return None, TransientException(f"Unsupported response type: {type(response).__name__}")