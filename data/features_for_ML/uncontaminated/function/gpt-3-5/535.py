def _prepare_cloning_inputs(
    clone_reference_filename: str,
    reference_audio_base_path: str,
    max_ref_duration_sec: float,
    whisper_model_name: str,
    whisper_cache_path: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    
    audio_prompt_tensor = None
    reference_transcript_text = None
    error_message = None
    
    # Implementation logic goes here
    
    return audio_prompt_tensor, reference_transcript_text