from dataclasses import dataclass
from typing import Dict

@dataclass
class ChatMood:
    chat_id: str
    mood: int

class MoodManager:
    def __init__(self):
        self.chat_moods: Dict[str, ChatMood] = {}

    def get_mood_by_chat_id(self, chat_id: str) -> ChatMood:
        if chat_id not in self.chat_moods:
            self.chat_moods[chat_id] = ChatMood(chat_id, 0)
        return self.chat_moods[chat_id]

    def reset_mood_by_chat_id(self, chat_id: str):
        if chat_id in self.chat_moods:
            self.chat_moods[chat_id].mood = 0