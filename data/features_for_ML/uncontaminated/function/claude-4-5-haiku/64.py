def audio_resample(data, config: DataConfig):
    """ Resample data.
        Inplace operation.
    """
    import librosa
    
    if config.sample_rate is None or config.sample_rate == data.sample_rate:
        return data
    
    # Resample audio data
    resampled_audio = librosa.resample(
        data.audio,
        orig_sr=data.sample_rate,
        target_sr=config.sample_rate
    )
    
    # Update audio and sample rate in place
    data.audio = resampled_audio
    data.sample_rate = config.sample_rate
    
    return data