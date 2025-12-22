def from_json(data: dict, bot) -> "MessageDeletePayload | None":
    if not data:
        return None
    
    return MessageDeletePayload(
        id=data.get("id"),
        channel_id=data.get("channel_id"),
        guild_id=data.get("guild_id"),
        bot=bot
    )