def greeting(
    querychat_config,
    *,
    generate: bool = True,
    stream: bool = False,
    **kwargs,
) -> str | None:
    """
    Generate or retrieve a greeting message.

    Use this function to generate a friendly greeting message using the chat
    client and data source specified in the `querychat_config` object. You can
    pass this greeting to `init()` to set an initial greeting for users for
    faster startup times and lower costs. If you don't provide a greeting in
    `init()`, one will be generated at the start of every new conversation.

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
        Additional arguments passed to the chat client's `chat()` or `stream_async()` method.

    Returns
    -------
    str | None
        - When `generate = False`: Returns the existing greeting as a string or
          `None` if no greeting exists.
        - When `generate = True`: Returns the chat response containing a greeting and
          sample prompts.

    Examples
    --------
    ```python
    import pandas as pd
    from querychat import init, greeting

    # Create config with mtcars dataset
    mtcars = pd.read_csv(
        "https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv"
    )
    mtcars_config = init(mtcars, "mtcars")

    # Generate a new greeting
    greeting_text = greeting(mtcars_config)

    # Update the config with the generated greeting
    mtcars_config = init(
        mtcars,
        "mtcars",
        greeting="Hello! I'm here to help you explore and analyze the mtcars...",
    )
    ```

    """
    if not generate:
        return getattr(querychat_config, "greeting", None)
    
    existing_greeting = getattr(querychat_config, "greeting", None)
    if existing_greeting:
        return existing_greeting
    
    chat_client = querychat_config.chat_client
    data_source_name = querychat_config.data_source_name
    
    greeting_prompt = f"Generate a friendly, concise greeting message for a user who is about to explore and analyze data from '{data_source_name}'. Include 2-3 sample questions they could ask. Keep it under 100 words."
    
    if stream:
        return chat_client.stream_async(greeting_prompt, **kwargs)
    else:
        return chat_client.chat(greeting_prompt, **kwargs)