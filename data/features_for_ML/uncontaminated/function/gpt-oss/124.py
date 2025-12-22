from __future__ import annotations

from typing import Any, Iterable, Union

def greeting(
    querychat_config,
    *,
    generate: bool = True,
    stream: bool = False,
    **kwargs,
) -> Union[str, Iterable[str], None]:
    """
    Generate or retrieve a greeting message.

    Parameters
    ----------
    querychat_config
        A QueryChatConfig object from `init()`.
    generate
        If `True` and if `querychat_config` does not include a `greeting`, a new
        greeting is generated. If `False`, returns the existing greeting from
        the configuration (if any).
    stream
        If `True`, returns a streaming response suitable for use in a Shiny app
        with `chat_ui.append_message_stream()`. If `False` (default), returns
        the full greeting at once. Only relevant when `generate = True`.
    **kwargs
        Additional arguments passed to the chat client's `chat()` or
        `stream_async()` method.

    Returns
    -------
    str | Iterable[str] | None
        - When `generate = False`: Returns the existing greeting as a string or
          `None` if no greeting exists.
        - When `generate = True`: Returns the chat response containing a greeting
          and sample prompts. If `stream=True`, an iterable of strings is
          returned.
    """
    # Helper to extract text from the chat client response
    def _extract_text(resp: Any) -> str:
        if isinstance(resp, str):
            return resp
        # Common patterns for chat responses
        if hasattr(resp, "content"):
            return getattr(resp, "content")
        if isinstance(resp, dict):
            # Try common keys
            for key in ("content", "text", "message", "response"):
                if key in resp:
                    return resp[key]
        # Fallback: convert to string
        return str(resp)

    # If we are not generating, just return the stored greeting (if any)
    if not generate:
        return getattr(querychat_config, "greeting", None)

    # If a greeting already exists, return it
    existing = getattr(querychat_config, "greeting", None)
    if existing:
        return existing

    # No greeting exists and we need to generate one
    # Determine the dataset name for the prompt
    dataset_name = getattr(querychat_config, "dataset_name", None)
    if dataset_name is None:
        # Try to infer from the data source if possible
        data_source = getattr(querychat_config, "data_source", None)
        if data_source is not None:
            dataset_name = getattr(data_source, "name", None)
    if not dataset_name:
        dataset_name = "the dataset"

    # Build the prompt for the chat client
    prompt = (
        f"Generate a friendly greeting message for users interacting with the "
        f"dataset '{dataset_name}'. The greeting should be concise, welcoming, "
        f"and include a few sample prompts that a user might ask about the "
        f"dataset. Keep the tone professional and helpful."
    )

    # Retrieve the chat client from the config
    client = getattr(querychat_config, "client", None)
    if client is None:
        raise ValueError("The querychat_config does not contain a chat client.")

    # Generate the greeting using the appropriate method
    if stream:
        # stream_async is expected to return an async generator or iterable
        stream_resp = client.stream_async(prompt, **kwargs)
        # If the returned object is async, we need to return it as is
        return stream_resp

    # Non-streaming case
    chat_resp = client.chat(prompt, **kwargs)
    greeting_text = _extract_text(chat_resp)
    return greeting_text