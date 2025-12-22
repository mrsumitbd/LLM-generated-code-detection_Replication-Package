from typing import List, Dict

class BaseMessage:
    def __init__(self, text: str, sender: str):
        self.text = text
        self.sender = sender

def _parse_old_conversations(old_conversations: List[Dict]) -> List[BaseMessage]:
    parsed_conversations = []
    for conversation in old_conversations:
        text = conversation.get('text', '')
        sender = conversation.get('sender', '')
        parsed_conversations.append(BaseMessage(text, sender))
    return parsed_conversations