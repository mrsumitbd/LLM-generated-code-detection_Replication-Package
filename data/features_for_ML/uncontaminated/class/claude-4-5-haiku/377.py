from typing import Dict
from dataclasses import dataclass
from enum import Enum

class MoodType(Enum):
    HAPPY = "happy"
    SAD = "sad"
    NEUTRAL = "neutral"
    ANGRY = "angry"
    EXCITED = "excited"

@dataclass
class ChatMood:
    chat_id: str
    mood_type: MoodType
    intensity: int

class MoodManager:

    def __init__(self):
        self._moods: Dict[str, ChatMood] = {}
        self._default_mood = ChatMood(
            chat_id="",
            mood_type=MoodType.NEUTRAL,
            intensity=5
        )

    def get_mood_by_chat_id(self, chat_id: str) -> ChatMood:
        if chat_id not in self._moods:
            mood = ChatMood(
                chat_id=chat_id,
                mood_type=MoodType.NEUTRAL,
                intensity=5
            )
            self._moods[chat_id] = mood
            return mood
        return self._moods[chat_id]

    def reset_mood_by_chat_id(self, chat_id: str):
        if chat_id in self._moods:
            self._moods[chat_id] = ChatMood(
                chat_id=chat_id,
                mood_type=MoodType.NEUTRAL,
                intensity=5
            )
        else:
            self._moods[chat_id] = ChatMood(
                chat_id=chat_id,
                mood_type=MoodType.NEUTRAL,
                intensity=5
            )

    def set_mood_by_chat_id(self, chat_id: str, mood_type: MoodType, intensity: int):
        self._moods[chat_id] = ChatMood(
            chat_id=chat_id,
            mood_type=mood_type,
            intensity=max(1, min(10, intensity))
        )

    def update_mood_intensity(self, chat_id: str, delta: int):
        mood = self.get_mood_by_chat_id(chat_id)
        new_intensity = max(1, min(10, mood.intensity + delta))
        mood.intensity = new_intensity

    def clear_all_moods(self):
        self._moods.clear()