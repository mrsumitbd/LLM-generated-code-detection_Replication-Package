class FrequencyControl:
    """Simple frequency control class to manage frequency values for different chat_ids"""

    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.talk_frequency_adjust = 1.0

    def get_talk_frequency_adjust(self) -> float:
        return self.talk_frequency_adjust

    def set_talk_frequency_adjust(self, value: float) -> None:
        self.talk_frequency_adjust = value

# Example usage:
# freq_control = FrequencyControl("example_chat_id")
# print(freq_control.get_talk_frequency_adjust())  # Output: 1.0
# freq_control.set_talk_frequency_adjust(1.5)
# print(freq_control.get_talk_frequency_adjust())  # Output: 1.5