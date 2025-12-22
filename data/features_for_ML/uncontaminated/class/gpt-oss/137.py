class FrequencyControl:
    """简化的频率控制类，仅管理不同chat_id的频率值"""

    _freq_map: dict[str, float] = {}

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        if chat_id not in self._freq_map:
            self._freq_map[chat_id] = 1.0

    def get_talk_frequency_adjust(self) -> float:
        return self._freq_map.get(self.chat_id, 1.0)

    def set_talk_frequency_adjust(self, value: float) -> None:
        self._freq_map[self.chat_id] = float(value)