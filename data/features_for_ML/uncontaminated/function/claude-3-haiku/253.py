from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MessageRecipient:
    name: str
    email: str
    phone: Optional[str]

def from_json(data: dict) -> "MessageRecipient":
    return MessageRecipient(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone", None)
    )