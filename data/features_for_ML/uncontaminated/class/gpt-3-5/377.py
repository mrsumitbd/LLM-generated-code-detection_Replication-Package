class ChatMood:
    def __init__(self, mood: str):
        self.mood = mood

class MoodManager:
    def __init__(self):
        self.mood_map = {}

    def get_mood_by_chat_id(self, chat_id: str) -> ChatMood:
        return self.mood_map.get(chat_id)

    def reset_mood_by_chat_id(self, chat_id: str):
        if chat_id in self.mood_map:
            del self.mood_map[chat_id]