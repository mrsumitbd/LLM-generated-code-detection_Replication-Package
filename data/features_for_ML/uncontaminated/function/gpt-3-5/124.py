def greeting(
    querychat_config,
    *,
    generate: bool = True,
    stream: bool = False,
    **kwargs,
) -> str | None:
    if generate:
        if "greeting" not in querychat_config:
            if stream:
                return querychat_config.chat(stream_async=True, **kwargs)
            else:
                return querychat_config.chat(**kwargs)
        else:
            return querychat_config["greeting"]
    else:
        return querychat_config.get("greeting", None)