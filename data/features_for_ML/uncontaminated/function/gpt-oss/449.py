from __future__ import annotations

def from_json(data: dict, bot) -> "MessageDeletePayload | None":
    """
    Parse a MESSAGE_DELETE payload from the Discord gateway.

    Parameters
    ----------
    data : dict
        The raw JSON payload from the gateway.
    bot : Bot
        The bot instance, used to resolve channel and guild objects.

    Returns
    -------
    MessageDeletePayload | None
        A payload object containing the message id, channel, guild and
        optionally the cached message.  Returns ``None`` if the payload
        cannot be parsed or the channel cannot be resolved.
    """
    # Basic validation of required keys
    if not isinstance(data, dict):
        return None

    # Extract and validate the message id
    msg_id_raw = data.get("id")
    if msg_id_raw is None:
        return None
    try:
        msg_id = int(msg_id_raw)
    except (TypeError, ValueError):
        return None

    # Extract and validate the channel id
    channel_id_raw = data.get("channel_id")
    if channel_id_raw is None:
        return None
    try:
        channel_id = int(channel_id_raw)
    except (TypeError, ValueError):
        return None

    # Resolve the channel object
    channel = bot.get_channel(channel_id)
    if channel is None:
        # If we cannot find the channel, we cannot construct a payload
        return None

    # Resolve the guild object if present
    guild_id_raw = data.get("guild_id")
    guild = None
    if guild_id_raw is not None:
        try:
            guild_id = int(guild_id_raw)
            guild = bot.get_guild(guild_id)
        except (TypeError, ValueError):
            guild = None

    # Attempt to fetch the cached message, if any
    # The exact attribute name may vary; try common patterns
    message = None
    if hasattr(channel, "messages"):
        # Some implementations store a dict of messages
        try:
            message = channel.messages.get(msg_id)
        except Exception:
            message = None
    elif hasattr(channel, "cache"):
        try:
            message = channel.cache.get(msg_id)
        except Exception:
            message = None

    # Construct the payload
    try:
        payload = MessageDeletePayload(
            message_id=msg_id,
            channel=channel,
            guild=guild,
            message=message,
        )
    except Exception:
        # If the payload constructor fails, return None
        return None

    return payload