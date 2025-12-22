class FrequencyControl:
    """简化的频率控制类，仅管理不同chat_id的频率值"""
    
    _frequency_storage = {}

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        if chat_id not in FrequencyControl._frequency_storage:
            FrequencyControl._frequency_storage[chat_id] = 1.0

    def get_talk_frequency_adjust(self) -> float:
        return FrequencyControl._frequency_storage.get(self.chat_id, 1.0)

    def set_talk_frequency_adjust(self, value: float) -> None:
        FrequencyControl._frequency_storage[self.chat_id] = value