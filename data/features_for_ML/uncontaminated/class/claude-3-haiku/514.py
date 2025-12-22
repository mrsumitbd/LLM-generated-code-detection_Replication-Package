class ADS1x15:
    "General ADS1x15 family ADC class"

    def __init__(self):
        self._input_channel = None
        self._gain_config = None
        self._mode_config = None
        self._data_rate = None
        self._comparator_mode = None
        self._comparator_polarity = None
        self._comparator_latch = None
        self._comparator_queue = None
        self._max_voltage = None

    def get_input(self):
        return self._input_channel

    def get_gain(self) -> GainConfig:
        return self._gain_config

    def get_mode(self) -> ModeConfig:
        return self._mode_config

    def get_data_rate(self) -> ADS101XDataRate | ADS111XDataRate:
        return self._data_rate

    def get_comparator_mode(self) -> ComparatorMode:
        return self._comparator_mode

    def get_comparator_polarity(self) -> ComparatorPolarity:
        return self._comparator_polarity

    def get_comparator_latch(self) -> ComparatorLatch:
        return self._comparator_latch

    def get_comparator_queue(self) -> ComparatorQueue:
        return self._comparator_queue

    def get_max_voltage(self) -> float:
        return self._max_voltage

    def to_voltage(self, value: int = 1) -> float:
        return value * self._max_voltage