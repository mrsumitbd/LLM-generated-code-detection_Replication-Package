def from_json(data: dict) -> "MessageRecipient":
    return MessageRecipient(
        recipient_id=data.get("recipient_id"),
        recipient_type=data.get("recipient_type"),
        recipient_name=data.get("recipient_name"),
        recipient_email=data.get("recipient_email"),
        recipient_phone=data.get("recipient_phone"),
        recipient_address=data.get("recipient_address"),
        recipient_metadata=data.get("recipient_metadata")
    )