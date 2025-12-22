class ChannelProcessor:
    """Complete channel processing pipeline."""

    def __init__(self) -> None:
        self.channel_processors = [
            self.remove_duplicates,
            self.convert_to_lowercase,
            self.remove_leading_trailing_whitespace,
            self.remove_empty_channels,
        ]

    def process_channels(self, raw_channels: list[str]) -> ChannelProcessingResult:
        processed_channels = raw_channels.copy()
        for processor in self.channel_processors:
            processed_channels = [processor(channel) for channel in processed_channels]

        return ChannelProcessingResult(processed_channels)

    @staticmethod
    def remove_duplicates(channel: str) -> str:
        return "".join(set(channel))

    @staticmethod
    def convert_to_lowercase(channel: str) -> str:
        return channel.lower()

    @staticmethod
    def remove_leading_trailing_whitespace(channel: str) -> str:
        return channel.strip()

    @staticmethod
    def remove_empty_channels(channel: str) -> str:
        return channel if channel else None

class ChannelProcessingResult:
    def __init__(self, processed_channels: list[str]) -> None:
        self.processed_channels = [channel for channel in processed_channels if channel is not None]