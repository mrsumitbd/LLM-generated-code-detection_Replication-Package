def from_json(data: dict) -> "MessageRecipient":
        if data is None:
            return None

        return MessageRecipient(
            chat_id=data["chat_id"], chat_type=data["chat_type"]
        )