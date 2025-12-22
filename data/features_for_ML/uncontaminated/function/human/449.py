def from_json(data: dict, bot) -> "MessageDeletePayload | None":
        if data is None:
            return None

        return MessageDeletePayload(
            data["timestamp"],
            bot.cache.get_message(data.get("message_id")),
            data.get("message_id"),
            data.get("chat_id"),
            data.get("user_id"),
            bot=bot,
        )