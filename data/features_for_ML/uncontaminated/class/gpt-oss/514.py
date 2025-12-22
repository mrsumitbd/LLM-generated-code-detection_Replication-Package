from __future__ import annotations
from enum import Enum, IntEnum
from typing import Union


class GainConfig(IntEnum):
    FS_6_144V = 0
    FS_4_096V = 1
    FS_2_048V = 2
    FS_1_024V = 3
    FS_0_512V = 4
    FS_0_256V = 5


class ModeConfig(IntEnum):
    CONTINUOUS = 0
    SINGLE = 1


class ADS101XDataRate(IntEnum):
    RATE_128SPS = 0
    RATE_250SPS = 1
    RATE_490SPS = 2
    RATE_920SPS = 3


class ADS111XDataRate(IntEnum):
    RATE_8SPS = 0
    RATE_16SPS = 1
    RATE_32SPS = 2
    RATE_64SPS = 3
    RATE_128SPS = 4
    RATE_250SPS = 5
    RATE_475SPS = 6
    RATE_860SPS = 7


class ComparatorMode(IntEnum):
    TRADITIONAL = 0
    WINDOW = 1


class ComparatorPolarity(IntEnum):
    ACTIVE_LOW = 0
    ACTIVE_HIGH = 1


class ComparatorLatch(IntEnum):
    NON_LATCHING = 0
    LATCHING = 1


class ComparatorQueue(IntEnum):
    ONE = 0
    TWO = 1
    FOUR = 2
    DISABLED = 3


class ADS1x15:
    """General ADS1x15 family ADC class"""

    _GAIN_TO_MAX_VOLTAGE = {
        GainConfig.FS_6_144V: 6.144,
        GainConfig.FS_4_096V: 4.096,
        GainConfig.FS_2_048V: 2.048,
        GainConfig.FS_1_024V: 1.024,
        GainConfig.FS_0_512V: 0.512,
        GainConfig.FS_0_256V: 0.256,
    }

    def __init__(self):
        self._input = 0
        self._gain = GainConfig.FS_2_048V
        self._mode = ModeConfig.CONTINUOUS
        self._data_rate: Union[ADS101XDataRate, ADS111XDataRate] = ADS111XDataRate.RATE_128SPS
        self._comparator_mode = ComparatorMode.TRADITIONAL
        self._comparator_polarity = ComparatorPolarity.ACTIVE_LOW
        self._comparator_latch = ComparatorLatch.NON_LATCHING
        self._comparator_queue = ComparatorQueue.DISABLED

    def get_input(self):
        return self._input

    def get_gain(self) -> GainConfig:
        return self._gain

    def get_mode(self) -> ModeConfig:
        return self._mode

    def get_data_rate(self) -> Union[ADS101XDataRate, ADS111XDataRate]:
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
        return self._GAIN_TO_MAX_VOLTAGE[self._gain]

    def to_voltage(self, value: int = 1) -> float:
        """Convert a raw ADC value to a voltage."""
        max_voltage = self.get_max_voltage()
        # ADS1x15 returns a signed 16‑bit value (two's complement)
        # Range: -32768 .. 32767
        return (value * max_voltage) / 32768.0