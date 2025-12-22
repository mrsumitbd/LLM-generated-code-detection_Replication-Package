class ChannelProcessingResult:
    def __init__(self, processed_channels: list[str], error_channels: list[str]):
        self.processed_channels = processed_channels
        self.error_channels = error_channels

class ChannelProcessor:
    def __init__(self) -> None:
        pass

    def process_channels(self, raw_channels: list[str]) -> ChannelProcessingResult:
        processed_channels = []
        error_channels = []

        for channel in raw_channels:
            if channel.startswith("valid_"):
                processed_channels.append(channel)
            else:
                error_channels.append(channel)

        return ChannelProcessingResult(processed_channels, error_channels)