def process_audio(audio_data=None):
    if audio_data is None:
        audio_data = decrypted
    
    import io
    from pydub import AudioSegment
    
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        
        duration_ms = len(audio)
        duration_sec = duration_ms / 1000.0
        
        frame_rate = audio.frame_rate
        channels = audio.channels
        sample_width = audio.sample_width
        
        result = {
            "duration_seconds": duration_sec,
            "frame_rate": frame_rate,
            "channels": channels,
            "sample_width": sample_width,
            "total_frames": int(duration_sec * frame_rate),
            "bitrate": audio.frame_rate * audio.channels * audio.sample_width * 8
        }
        
        return result
    
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }