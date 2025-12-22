def prepare_sample_waveforms(audio_paths, cuda_enabled=True, sr=TARGET_SAMPLE_RATE, max_length_seconds=10):
    """
    Prepare sample waveforms from audio file paths.
    
    Args:
        audio_paths: List of paths to audio files
        cuda_enabled: Whether to use CUDA for processing
        sr: Sample rate for loading audio
        max_length_seconds: Maximum length of audio in seconds
        
    Returns:
        List of preprocessed waveforms as tensors
    """
    import torchaudio
    import torch
    
    waveforms = []
    max_samples = int(sr * max_length_seconds)
    
    for audio_path in audio_paths:
        try:
            # Load audio file
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Resample if necessary
            if sample_rate != sr:
                resampler = torchaudio.transforms.Resample(sample_rate, sr)
                waveform = resampler(waveform)
            
            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            # Truncate or pad to max length
            if waveform.shape[1] > max_samples:
                waveform = waveform[:, :max_samples]
            elif waveform.shape[1] < max_samples:
                padding = max_samples - waveform.shape[1]
                waveform = torch.nn.functional.pad(waveform, (0, padding))
            
            # Move to GPU if enabled
            if cuda_enabled and torch.cuda.is_available():
                waveform = waveform.cuda()
            
            waveforms.append(waveform)
            
        except Exception as e:
            print(f"Error loading audio file {audio_path}: {e}")
            continue
    
    return waveforms