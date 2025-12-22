class EnhancedAudioDetector:
    """
    Advanced audio detection using comprehensive metadata analysis.
    Based on successful patterns from Enhanced Resolution Detection.
    """

    def __init__(self, patterns: Optional[DetectionPatterns] = None):
        self.patterns = patterns or DetectionPatterns()

    def extract_audio_info(self, media_item: Dict[str, Any]) -> Optional[AudioInfo]:
        audio_stream = self._find_primary_audio_stream(media_item)
        if not audio_stream:
            return None

        audio_format = self._detect_audio_format(audio_stream)
        channels = audio_stream.get('channels', 2)
        channel_layout = self._detect_channel_layout(channels, audio_format)
        bitrate = self._extract_bitrate(audio_stream)
        quality_score = self._calculate_audio_quality_score(audio_stream)

        return AudioInfo(
            format=audio_format,
            channels=channels,
            channel_layout=channel_layout,
            bitrate=bitrate,
            is_lossless=self._detect_lossless(audio_stream),
            is_atmos=self._detect_atmos(audio_stream),
            is_dts_x=self._detect_dts_x(audio_stream),
            is_object_based=self._detect_object_based(audio_stream),
            quality_score=quality_score,
            language=audio_stream.get('language', 'unknown'),
            title=audio_stream.get('title', '')
        )

    def _find_primary_audio_stream(self, media_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        streams = media_item.get('streams', [])
        audio_streams = [s for s in streams if s.get('type') == 'audio']

        if not audio_streams:
            return None

        # Prioritize by language and codec quality
        default_lang = media_item.get('default_language', 'eng')
        for stream in audio_streams:
            if stream.get('language') == default_lang or stream.get('default'):
                return stream

        return audio_streams[0]

    def _calculate_audio_quality_score(self, audio_stream: Dict[str, Any]) -> int:
        score = 0

        # Codec quality
        codec = audio_stream.get('codec', '').lower()
        if 'flac' in codec or 'pcm' in codec:
            score += 100
        elif 'truehd' in codec or 'dts-hd' in codec:
            score += 90
        elif 'dts' in codec or 'ac3' in codec or 'eac3' in codec:
            score += 70
        elif 'aac' in codec or 'mp3' in codec:
            score += 50
        else:
            score += 30

        # Bitrate quality
        bitrate = self._extract_bitrate(audio_stream)
        if bitrate:
            if bitrate >= 640:
                score += 30
            elif bitrate >= 320:
                score += 20
            elif bitrate >= 128:
                score += 10

        # Channel configuration
        channels = audio_stream.get('channels', 2)
        if channels >= 8:
            score += 20
        elif channels >= 6:
            score += 15
        elif channels >= 2:
            score += 5

        # Object-based audio
        if self._detect_object_based(audio_stream):
            score += 25

        return min(score, 255)

    def _detect_audio_format(self, audio_stream: Dict[str, Any]) -> AudioFormat:
        codec = audio_stream.get('codec', '').lower()
        codec_name = audio_stream.get('codec_name', '').lower()

        codec_str = f"{codec} {codec_name}".lower()

        if any(pattern in codec_str for pattern in self.patterns.flac_patterns):
            return AudioFormat.FLAC
        elif any(pattern in codec_str for pattern in self.patterns.truehd_patterns):
            return AudioFormat.TRUEHD
        elif any(pattern in codec_str for pattern in self.patterns.dts_hd_patterns):
            return AudioFormat.DTS_HD
        elif any(pattern in codec_str for pattern in self.patterns.dts_patterns):
            return AudioFormat.DTS
        elif any(pattern in codec_str for pattern in self.patterns.eac3_patterns):
            return AudioFormat.EAC3
        elif any(pattern in codec_str for pattern in self.patterns.ac3_patterns):
            return AudioFormat.AC3
        elif any(pattern in codec_str for pattern in self.patterns.aac_patterns):
            return AudioFormat.AAC
        elif any(pattern in codec_str for pattern in self.patterns.mp3_patterns):
            return AudioFormat.MP3
        elif any(pattern in codec_str for pattern in self.patterns.opus_patterns):
            return AudioFormat.OPUS
        elif any(pattern in codec_str for pattern in self.patterns.vorbis_patterns):
            return AudioFormat.VORBIS
        elif any(pattern in codec_str for pattern in self.patterns.pcm_patterns):
            return AudioFormat.PCM
        else:
            return AudioFormat.UNKNOWN

    def _detect_atmos(self, audio_stream: Dict[str, Any]) -> bool:
        codec = audio_stream.get('codec', '').lower()
        codec_name = audio_stream.get('codec_name', '').lower()
        title = audio_stream.get('title', '').lower()
        profile = audio_stream.get('profile', '').lower()

        search_str = f"{codec} {codec_name} {title} {profile}".lower()

        return any(pattern in search_str for pattern in self.patterns.atmos_patterns)

    def _detect_dts_x(self, audio_stream: Dict[str, Any]) -> bool:
        codec = audio_stream.get('codec', '').lower()
        codec_name = audio_stream.get('codec_name', '').lower()
        title = audio_stream.get('title', '').lower()
        profile = audio_stream.get('profile', '').lower()

        search_str = f"{codec} {codec_name} {title} {profile}".lower()

        return any(pattern in search_str for pattern in self.patterns.dts_x_patterns)

    def _detect_lossless(self, audio_stream: Dict[str, Any]) -> bool:
        audio_format = self._detect_audio_format(audio_stream)
        lossless_formats = {
            AudioFormat.FLAC,
            AudioFormat.TRUEHD,
            AudioFormat.DTS_HD,
            AudioFormat.PCM
        }
        return audio_format in lossless_formats

    def _detect_object_based(self, audio_stream: Dict[str, Any]) -> bool:
        return self._detect_atmos(audio_stream) or self._detect_dts_x(audio_stream)

    def _detect_channel_layout(self, channels: int, audio_format: AudioFormat) -> ChannelLayout:
        if channels == 1:
            return ChannelLayout.MONO
        elif channels == 2:
            return ChannelLayout.STEREO
        elif channels == 6:
            return ChannelLayout.SURROUND_5_1
        elif channels == 8:
            return ChannelLayout.SURROUND_7_1
        elif channels >= 10:
            return ChannelLayout.SURROUND_7_1_4
        else:
            return ChannelLayout.UNKNOWN

    def _extract_bitrate(self, audio_stream: Dict[str, Any]) -> Optional[int]:
        bitrate = audio_stream.get('bit_rate')
        if bitrate:
            if isinstance(bitrate, str):
                bitrate_str = bitrate.lower().replace('kbps', '').replace('k', '').strip()
                try:
                    return int(float(bitrate_str))
                except (ValueError, AttributeError):
                    return None
            else:
                return int(bitrate / 1000) if bitrate >= 1000 else bitrate

        return None