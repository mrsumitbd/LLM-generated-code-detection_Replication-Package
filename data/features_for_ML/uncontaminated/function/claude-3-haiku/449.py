def from_json(data: dict, bot) -> "MessageDeletePayload | None":
    try:
        channel_id = int(data.get("channel_id"))
        message_id = int(data.get("message_id"))
        user_id = int(data.get("user_id"))
        guild_id = int(data.get("guild_id"))

        channel = bot.get_channel(channel_id)
        if channel is None:
            return None

        message = yield from channel.get_message(message_id)
        if message is None:
            return None

        return MessageDeletePayload(
            channel=channel,
            message=message,
            user_id=user_id,
            guild_id=guild_id
        )
    except (ValueError, TypeError):
        return None