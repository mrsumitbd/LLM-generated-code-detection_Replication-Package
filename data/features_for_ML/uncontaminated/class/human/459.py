from speech_mcp.tts_adapters import KokoroTTS
from speech_mcp.tts_adapters import KokoroTTS, Pyttsx3TTS
from speech_mcp.tts_adapters import Pyttsx3TTS
from speech_mcp.tts_adapters import Pyttsx3TTS
from speech_mcp.tts_adapters import KokoroTTS

class VoiceInstance:
    """Manages a single Kokoro TTS voice instance"""
    def __init__(self, voice_id: str):
        from speech_mcp.tts_adapters import KokoroTTS
        self.engine = None
        self.fallback_engine = None
        self.voice_id = voice_id
        
        logger.info(f"Initializing VoiceInstance for voice: {voice_id}")
        
        # Try to initialize Kokoro
        try:
            logger.info("Attempting to initialize Kokoro TTS...")
            self.engine = KokoroTTS(voice=voice_id, lang_code="a", speed=1.0)
            logger.info(f"Kokoro TTS initialized: is_initialized={self.engine.is_initialized}, kokoro_available={self.engine.kokoro_available}")
            if self.engine.is_initialized and self.engine.kokoro_available:
                logger.info("Kokoro TTS initialization successful")
                return  # Successfully initialized
            else:
                logger.warning("Kokoro TTS initialization incomplete")
        except Exception as e:
            logger.warning(f"Failed to initialize Kokoro TTS for voice {voice_id}: {str(e)}")
            self.engine = None
            
        # Try fallback if Kokoro failed
        try:
            logger.info("Attempting to initialize fallback TTS...")
            from speech_mcp.tts_adapters import Pyttsx3TTS
            self.fallback_engine = Pyttsx3TTS(lang_code="en", speed=1.0)
            logger.info(f"Fallback TTS initialized: is_initialized={self.fallback_engine.is_initialized}")
            if self.fallback_engine.is_initialized:
                logger.info("Fallback TTS initialization successful")
                return  # Successfully initialized fallback
            else:
                logger.warning("Fallback TTS initialization incomplete")
        except Exception as e:
            logger.warning(f"Failed to initialize fallback TTS: {str(e)}")
            self.fallback_engine = None
        
        # If both Kokoro and fallback failed, raise exception
        if self.engine is None and self.fallback_engine is None:
            logger.error("Both Kokoro and fallback TTS initialization failed")
            raise Exception(f"Failed to initialize any TTS engine for voice {voice_id}")
        
        # If initialization succeeded but voice isn't available, show available voices
        available_voices = []
        if self.engine and self.engine.kokoro_available:
            available_voices = self.engine.get_available_voices()
            logger.info(f"Got {len(available_voices)} available voices from Kokoro")
        elif self.fallback_engine:
            available_voices = self.fallback_engine.get_available_voices()
            logger.info(f"Got {len(available_voices)} available voices from fallback")
            
        if available_voices and voice_id not in available_voices:
            logger.warning(f"Requested voice {voice_id} not found in available voices")
            voice_categories = {
                "American Female": [v for v in available_voices if v.startswith("af_")],
                "American Male": [v for v in available_voices if v.startswith("am_")],
                "British Female": [v for v in available_voices if v.startswith("bf_")],
                "British Male": [v for v in available_voices if v.startswith("bm_")],
                "Other English": [v for v in available_voices if v.startswith(("ef_", "em_"))],
                "French": [v for v in available_voices if v.startswith("ff_")],
                "Hindi": [v for v in available_voices if v.startswith(("hf_", "hm_"))],
                "Italian": [v for v in available_voices if v.startswith(("if_", "im_"))],
                "Japanese": [v for v in available_voices if v.startswith(("jf_", "jm_"))],
                "Portuguese": [v for v in available_voices if v.startswith(("pf_", "pm_"))],
                "Chinese": [v for v in available_voices if v.startswith(("zf_", "zm_"))]
            }
            
            # Build error message
            error_msg = [f"Voice '{voice_id}' not found. Available voices:"]
            for category, voices in voice_categories.items():
                if voices:  # Only show categories that have voices
                    error_msg.append(f"\n{category}:")
                    error_msg.append("  " + ", ".join(sorted(voices)))
            
            raise Exception("\n".join(error_msg))
        
    def generate_audio(self, text: str, output_path: str) -> bool:
        """Generate audio for the given text"""
        logger.info(f"Generating audio for text: '{text[:50]}...' with voice {self.voice_id}")
        
        # Try Kokoro first
        if self.engine and self.engine.kokoro_available:
            try:
                logger.info("Attempting to generate audio with Kokoro TTS...")
                result = self.engine.save_to_file(text, output_path)
                if result:
                    logger.info("Successfully generated audio with Kokoro TTS")
                    return True
                else:
                    logger.warning("Kokoro TTS save_to_file returned False")
            except Exception as e:
                logger.warning(f"Kokoro TTS failed to generate audio: {str(e)}")
        else:
            logger.info("Kokoro TTS not available for audio generation")
        
        # Try fallback if available
        if self.fallback_engine:
            try:
                logger.info("Attempting to generate audio with fallback TTS...")
                result = self.fallback_engine.save_to_file(text, output_path)
                if result:
                    logger.info("Successfully generated audio with fallback TTS")
                    return True
                else:
                    logger.warning("Fallback TTS save_to_file returned False")
            except Exception as e:
                logger.warning(f"Fallback TTS failed to generate audio: {str(e)}")
        else:
            logger.info("Fallback TTS not available for audio generation")
        
        # If both failed, raise exception with available voices info
        logger.error("Both Kokoro and fallback TTS failed to generate audio")
        
        # Get available voices from whichever engine is working
        available_voices = []
        if self.engine and self.engine.kokoro_available:
            available_voices = self.engine.get_available_voices()
            logger.info(f"Got {len(available_voices)} available voices from Kokoro")
        elif self.fallback_engine:
            available_voices = self.fallback_engine.get_available_voices()
            logger.info(f"Got {len(available_voices)} available voices from fallback")
        
        voice_categories = {
            "American Female": [v for v in available_voices if v.startswith("af_")],
            "American Male": [v for v in available_voices if v.startswith("am_")],
            "British Female": [v for v in available_voices if v.startswith("bf_")],
            "British Male": [v for v in available_voices if v.startswith("bm_")],
            "Other English": [v for v in available_voices if v.startswith(("ef_", "em_"))],
            "French": [v for v in available_voices if v.startswith("ff_")],
            "Hindi": [v for v in available_voices if v.startswith(("hf_", "hm_"))],
            "Italian": [v for v in available_voices if v.startswith(("if_", "im_"))],
            "Japanese": [v for v in available_voices if v.startswith(("jf_", "jm_"))],
            "Portuguese": [v for v in available_voices if v.startswith(("pf_", "pm_"))],
            "Chinese": [v for v in available_voices if v.startswith(("zf_", "zm_"))]
        }
        
        error_msg = [f"Failed to generate audio with voice '{self.voice_id}'. Available voices:"]
        for category, voices in voice_categories.items():
            if voices:
                error_msg.append(f"\n{category}:")
                error_msg.append("  " + ", ".join(sorted(voices)))
        
        raise Exception("\n".join(error_msg))