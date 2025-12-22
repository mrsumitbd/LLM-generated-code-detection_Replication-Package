import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class ChannelProcessingResult:
    """Result of processing channels."""
    processed_channels: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ChannelProcessor:
    """Complete channel processing pipeline."""

    # Regex pattern for a valid channel name (e.g., starts with '#' and contains alphanumerics or underscores)
    _CHANNEL_PATTERN = re.compile(r"^#\w+$")

    def __init__(self) -> None:
        # Any initialization logic can be added here
        pass

    def process_channels(self, raw_channels: List[str]) -> ChannelProcessingResult:
        """
        Process a list of raw channel strings.

        Each channel is stripped of surrounding whitespace, converted to lowercase,
        and validated against a simple pattern. Valid channels are collected in
        `processed_channels`; invalid ones are recorded in `errors`.

        Args:
            raw_channels: List of raw channel strings.

        Returns:
            ChannelProcessingResult containing processed channels and any errors.
        """
        result = ChannelProcessingResult()

        for idx, raw in enumerate(raw_channels):
            cleaned = raw.strip().lower()
            if not cleaned:
                result.errors.append(f"Channel at index {idx} is empty after stripping.")
                continue

            if not self._CHANNEL_PATTERN.match(cleaned):
                result.errors.append(
                    f"Channel '{raw}' (cleaned: '{cleaned}') does not match pattern."
                )
                continue

            result.processed_channels.append(cleaned)

        return result