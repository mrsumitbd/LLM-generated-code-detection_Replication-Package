class ADS1x15:
    "General ADS1x15 family ADC class"

    def __init__(self):
        self._input = None
        self._gain = GainConfig.GAIN_ONE
        self._mode = ModeConfig.CONTINUOUS
        self._data_rate = None
        self._comparator_mode = ComparatorMode.TRADITIONAL
        self._comparator_polarity = ComparatorPolarity.ACTIVE_LOW
        self._comparator_latch = ComparatorLatch.NON_LATCHING
        self._comparator_queue = ComparatorQueue.DISABLE
        self._max_voltage = 4.096
        self._i2c = None
        self._address = None

    def get_input(self):
        return self._input

    def get_gain(self) -> GainConfig:
        return self._gain

    def get_mode(self) -> ModeConfig:
        return self._mode

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
        return (value * self._max_voltage) / 32767.0