def from_json(data: dict, bot) -> "MessageDeletePayload | None":
    if data.get('type') == 'message_delete':
        return MessageDeletePayload(data['message_id'], bot)
    return None