from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

# ----------------------------------------------------------------------
# Helper enums and dataclasses
# ----------------------------------------------------------------------
class AudioFormat(Enum):
    UNKNOWN = auto()
    AAC = auto()
    MP3 = auto()
    AC3 = auto()
    DTS = auto()
    FLAC = auto()
    ALAC = auto()
    WAV = auto()
    OTHER = auto()


class ChannelLayout(Enum):
    MONO = auto()
    STEREO = auto()
    FIVE_POINT_ONE = auto()
    SEVEN_POINT_ONE = auto()
    OTHER = auto()


@dataclass
class AudioInfo:
    format: AudioFormat
    quality_score: int
    atmos: bool
    dts_x: bool
    lossless: bool
    object_based: bool
    channel_layout: ChannelLayout
    bitrate: Optional[int]


# ----------------------------------------------------------------------
# Main class
# ----------------------------------------------------------------------
class EnhancedAudioDetector:
    """
    Advanced audio detection using comprehensive metadata analysis.
    Based on successful patterns from Enhanced Resolution Detection.
    """

    def __init__(self, patterns: Optional[Any] = None):
        # patterns are not used in this simplified implementation
        self.patterns = patterns

    def extract_audio_info(self, media_item: Dict[str, Any]) -> Optional[AudioInfo]:
        """
        Extract audio information from a media item dictionary.
        """
        audio_stream = self._find_primary_audio_stream(media_item)
        if not audio_stream:
            return None

        quality_score = self._calculate_audio_quality_score(audio_stream)
        audio_format = self._detect_audio_format(audio_stream)
        atmos = self._detect_atmos(audio_stream)
        dts_x = self._detect_dts_x(audio_stream)
        lossless = self._detect_lossless(audio_stream)
        object_based = self._detect_object_based(audio_stream)
        channel_layout = self._detect_channel_layout(
            audio_stream.get("channels", 0), audio_format
        )
        bitrate = self._extract_bitrate(audio_stream)

        return AudioInfo(
            format=audio_format,
            quality_score=quality_score,
            atmos=atmos,
            dts_x=dts_x,
            lossless=lossless,
            object_based=object_based,
            channel_layout=channel_layout,
            bitrate=bitrate,
        )

    def _find_primary_audio_stream(self, media_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find the first audio stream in the media item.
        """
        streams: List[Dict[str, Any]] = media_item.get("streams", [])
        for stream in streams:
            if stream.get("codec_type") == "audio":
                return stream
        return None

    def _calculate_audio_quality_score(self, audio_stream: Dict[str, Any]) -> int:
        """
        Calculate a simple quality score based on bitrate and channel count.
        """
        bitrate = audio_stream.get("bitrate")
        channels = audio_stream.get("channels", 0)
        if bitrate is None:
            bitrate = 0
        # Base score: bitrate in kbps + 10 points per channel
        return int(bitrate / 1000) + channels * 10

    def _detect_audio_format(self, audio_stream: Dict[str, Any]) -> AudioFormat:
        """
        Detect the audio format from the codec name.
        """
        codec = audio_stream.get("codec_name", "").lower()
        if "aac" in codec:
            return AudioFormat.AAC
        if "mp3" in codec:
            return AudioFormat.MP3
        if "ac3" in codec:
            return AudioFormat.AC3
        if "dts" in codec:
            return AudioFormat.DTS
        if "flac" in codec:
            return AudioFormat.FLAC
        if "alac" in codec:
            return AudioFormat.ALAC
        if "wav" in codec:
            return AudioFormat.WAV
        return AudioFormat.OTHER

    def _detect_atmos(self, audio_stream: Dict[str, Any]) -> bool:
        """
        Detect Dolby Atmos support.
        """
        profile = audio_stream.get("profile", "").lower()
        tags = audio_stream.get("tags", {})
        return "atmos" in profile or "dolby atmos" in tags.get("description", "").lower()

    def _detect_dts_x(self, audio_stream: Dict[str, Any]) -> bool:
        """
        Detect DTS:X format.
        """
        codec = audio_stream.get("codec_name", "").lower()
        profile = audio_stream.get("profile", "").lower()
        return "dts" in codec and "x" in profile

    def _detect_lossless(self, audio_stream: Dict[str, Any]) -> bool:
        """
        Detect lossless audio codecs or high bitrate.
        """
        codec = audio_stream.get("codec_name", "").lower()
        bitrate = audio_stream.get("bitrate")
        if codec in {"flac", "alac", "wav"}:
            return True
        if bitrate and bitrate > 1000_000:  # > 1000 kbps
            return True
        return False

    def _detect_object_based(self, audio_stream: Dict[str, Any]) -> bool:
        """
        Detect object‑based audio (e.g., AC‑3 object‑based).
        """
        codec = audio_stream.get("codec_name", "").lower()
        profile = audio_stream.get("profile", "").lower()
        return codec == "ac3" and "object" in profile

    def _detect_channel_layout(self, channels: int, audio_format: AudioFormat) -> ChannelLayout:
        """
        Determine channel layout based on channel count and format.
        """
        if channels == 1:
            return ChannelLayout.MONO
        if channels == 2:
            return ChannelLayout.STEREO
        if channels == 6:
            return ChannelLayout.FIVE_POINT_ONE
        if channels == 8:
            return ChannelLayout.SEVEN_POINT_ONE
        # For some formats, 6 channels might be 5.1, but we keep it simple
        return ChannelLayout.OTHER

    def _extract_bitrate(self, audio_stream: Dict[str, Any]) -> Optional[int]:
        """
        Extract bitrate from the audio stream metadata.
        """
        return audio_stream.get("bitrate")