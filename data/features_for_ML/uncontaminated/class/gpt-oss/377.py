from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class ChatMood:
    mood: str = "neutral"
    last_updated: datetime = field(default_factory=datetime.utcnow)


class MoodManager:
    def __init__(self) -> None:
        self._moods: Dict[str, ChatMood] = {}

    def get_mood_by_chat_id(self, chat_id: str) -> ChatMood:
        if chat_id not in self._moods:
            self._moods[chat_id] = ChatMood()
        return self._moods[chat_id]

    def reset_mood_by_chat_id(self, chat_id: str) -> None:
        self._moods[chat_id] = ChatMood()