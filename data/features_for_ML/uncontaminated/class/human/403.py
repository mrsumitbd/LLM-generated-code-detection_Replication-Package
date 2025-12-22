
class ChannelProcessor:
    """Complete channel processing pipeline."""

    def __init__(self) -> None:
        """Initialize channel processor with mapper, validator, and selector."""
        self.mapper = ChannelMapper()
        self.validator = ChannelValidator()
        self.selector = ChannelSelector()

    def process_channels(self, raw_channels: list[str]) -> ChannelProcessingResult:
        """Process channels through complete pipeline.

        Args:
            raw_channels: Raw channel names from EEG file

        Returns:
            ChannelProcessingResult with all processing details
        """
        # Step 1: Standardize names
        standardized = self.mapper.standardize_channel_names(raw_channels)

        # Step 2: Validate
        is_valid, missing = self.validator.validate_channels(standardized)

        # Step 3: Select and reorder
        selected, indices = self.selector.select_standard_channels(standardized)

        return ChannelProcessingResult(
            is_valid=is_valid,
            standardized_names=standardized,
            selected_indices=indices,
            missing_channels=missing,
            selected_channels=selected,
        )