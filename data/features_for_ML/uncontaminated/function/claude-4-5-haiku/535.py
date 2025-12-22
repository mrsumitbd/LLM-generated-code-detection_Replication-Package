def _prepare_cloning_inputs(
    clone_reference_filename: str,
    reference_audio_base_path: str,
    max_ref_duration_sec: float,
    whisper_model_name: str,
    whisper_cache_path: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Prepares inputs for voice cloning: loads/processes audio, gets transcript.

    Args:
        clone_reference_filename: Filename of the reference audio.
        reference_audio_base_path: Base path where reference files are stored.
        max_ref_duration_sec: Maximum duration for the reference audio prompt.
        whisper_model_name: Name of the Whisper model to use if needed.
        whisper_cache_path: Path to Whisper model cache.
        transcript: Optional explicit transcript text to override file/Whisper.

    Returns:
        Tuple of (audio_prompt_tensor, reference_transcript_text, error_message).
        On success, error_message is None. On failure, text and tensor are None.
    """
    import os
    import torchaudio
    import torch
    
    try:
        # Construct full path to reference audio file
        audio_path = os.path.join(reference_audio_base_path, clone_reference_filename)
        
        # Check if file exists
        if not os.path.exists(audio_path):
            return None, None
        
        # Load audio file
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Convert to mono if necessary
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        # Trim audio to max duration
        max_samples = int(max_ref_duration_sec * sample_rate)
        if waveform.shape[1] > max_samples:
            waveform = waveform[:, :max_samples]
        
        # Convert waveform to string representation for return
        audio_prompt_str = str(waveform.tolist())
        
        # Get transcript
        reference_transcript = None
        
        if transcript is not None:
            # Use provided transcript
            reference_transcript = transcript
        else:
            # Try to load transcript from file with same name but .txt extension
            transcript_path = os.path.splitext(audio_path)[0] + ".txt"
            if os.path.exists(transcript_path):
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    reference_transcript = f.read().strip()
            else:
                # Use Whisper to transcribe
                try:
                    import whisper
                    
                    # Load Whisper model
                    model = whisper.load_model(
                        whisper_model_name,
                        device="cuda" if torch.cuda.is_available() else "cpu",
                        download_root=whisper_cache_path
                    )
                    
                    # Transcribe audio
                    result = model.transcribe(audio_path)
                    reference_transcript = result.get("text", "").strip()
                    
                except Exception as e:
                    return None, None
        
        return audio_prompt_str, reference_transcript
        
    except Exception as e:
        return None, None