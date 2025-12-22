from enum import Enum

class GainConfig(Enum):
    GAIN_TWOTHIRDS = 0x0000
    GAIN_ONE = 0x0200
    GAIN_TWO = 0x0400
    GAIN_FOUR = 0x0600
    GAIN_EIGHT = 0x0800
    GAIN_SIXTEEN = 0x0A00

class ModeConfig(Enum):
    MODE_CONTINUOUS = 0x0000
    MODE_SINGLE = 0x0100

class ADS101XDataRate(Enum):
    DR_128SPS = 0x0000
    DR_250SPS = 0x0020
    DR_490SPS = 0x0040
    DR_920SPS = 0x0060
    DR_1600SPS = 0x0080
    DR_2400SPS = 0x00A0
    DR_3300SPS = 0x00C0

class ADS111XDataRate(Enum):
    DR_8SPS = 0x0000
    DR_16SPS = 0x0020
    DR_32SPS = 0x0040
    DR_64SPS = 0x0060
    DR_128SPS = 0x0080
    DR_250SPS = 0x00A0
    DR_475SPS = 0x00C0
    DR_860SPS = 0x00E0

class ComparatorMode(Enum):
    TRADITIONAL = 0x0000
    WINDOW = 0x0010

class ComparatorPolarity(Enum):
    ACTIVE_LOW = 0x0000
    ACTIVE_HIGH = 0x0008

class ComparatorLatch(Enum):
    NON_LATCHING = 0x0000
    LATCHING = 0x0004

class ComparatorQueue(Enum):
    ASSERT_AFTER_1 = 0x0000
    ASSERT_AFTER_2 = 0x0001
    ASSERT_AFTER_4 = 0x0002
    DISABLE_COMPARATOR = 0x0003

class ADS1x15:
    "General ADS1x15 family ADC class"

    def __init__(self):
        pass

    def get_input(self):
        pass

    def get_gain(self) -> GainConfig:
        pass

    def get_mode(self) -> ModeConfig:
        pass

    def get_data_rate(self) -> ADS101XDataRate | ADS111XDataRate:
        pass

    def get_comparator_mode(self) -> ComparatorMode:
        pass

    def get_comparator_polarity(self) -> ComparatorPolarity:
        pass

    def get_comparator_latch(self) -> ComparatorLatch:
        pass

    def get_comparator_queue(self) -> ComparatorQueue:
        pass

    def get_max_voltage(self) -> float:
        pass

    def to_voltage(self, value: int = 1) -> float:
        pass