class FrequencyControl:
    """简化的频率控制类，仅管理不同chat_id的频率值"""

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.talk_frequency_adjust = 1.0

    def get_talk_frequency_adjust(self) -> float:
        return self.talk_frequency_adjust

    def set_talk_frequency_adjust(self, value: float) -> None:
        self.talk_frequency_adjust = value