def from_json(data: dict) -> "MessageRecipient":
    recipient = MessageRecipient(data['name'], data['email'])
    return recipient