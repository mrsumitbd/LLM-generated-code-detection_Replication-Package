class ChannelProcessor:
    """Complete channel processing pipeline."""

    def __init__(self) -> None:
        pass

    def process_channels(self, raw_channels: list[str]) -> ChannelProcessingResult:
        processed_channels = []
        errors = []
        
        for channel in raw_channels:
            try:
                # Validate channel format
                if not isinstance(channel, str):
                    errors.append(f"Invalid channel type: {type(channel)}")
                    continue
                
                # Strip whitespace
                channel = channel.strip()
                
                # Check if empty
                if not channel:
                    errors.append("Empty channel name")
                    continue
                
                # Validate channel name (alphanumeric, underscore, hyphen)
                if not all(c.isalnum() or c in '_-' for c in channel):
                    errors.append(f"Invalid characters in channel: {channel}")
                    continue
                
                # Check length constraints
                if len(channel) < 1 or len(channel) > 80:
                    errors.append(f"Channel name length out of bounds: {channel}")
                    continue
                
                processed_channels.append(channel)
                
            except Exception as e:
                errors.append(f"Error processing channel '{channel}': {str(e)}")
        
        return ChannelProcessingResult(
            channels=processed_channels,
            errors=errors,
            success=len(errors) == 0
        )