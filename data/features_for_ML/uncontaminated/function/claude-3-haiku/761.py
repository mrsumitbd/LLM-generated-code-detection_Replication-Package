from typing import List, Dict
from .base_message import BaseMessage

def _parse_old_conversations(old_conversations: List[Dict]) -> List[BaseMessage]:
    messages = []
    for conversation in old_conversations:
        for message in conversation['messages']:
            msg = BaseMessage(
                id=message['id'],
                sender=message['sender'],
                timestamp=message['timestamp'],
                content=message['content']
            )
            messages.append(msg)
    return messages