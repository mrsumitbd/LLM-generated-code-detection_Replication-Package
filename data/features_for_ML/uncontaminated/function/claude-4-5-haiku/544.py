def log_mel_spectrogram(
    audio: Union[str, np.ndarray, torch.Tensor],
    n_mels: int = 80,
    padding: int = 0,
    device: Optional[Union[str, torch.device]] = None,
):
    """
    Compute the log-Mel spectrogram of

    Parameters
    ----------
    audio: Union[str, np.ndarray, torch.Tensor], shape = (*)
        The path to audio or either a NumPy array or Tensor containing the audio waveform in 16 kHz

    n_mels: int
        The number of Mel-frequency filters, only 80 and 128 are supported

    padding: int
        Number of zero samples to pad to the right

    device: Optional[Union[str, torch.device]]
        If given, the audio tensor is moved to this device before STFT

    Returns
    -------
    torch.Tensor, shape = (n_mels, n_frames)
        A Tensor that contains the Mel spectrogram
    """
    if isinstance(audio, str):
        import librosa
        audio, sr = librosa.load(audio, sr=16000)
        audio = torch.from_numpy(audio).float()
    elif isinstance(audio, np.ndarray):
        audio = torch.from_numpy(audio).float()
    elif isinstance(audio, torch.Tensor):
        audio = audio.float()
    else:
        raise TypeError(f"Unsupported audio type: {type(audio)}")
    
    if device is not None:
        audio = audio.to(device)
    
    if padding > 0:
        audio = torch.nn.functional.pad(audio, (0, padding))
    
    window = torch.hann_window(400)
    if device is not None:
        window = window.to(device)
    
    stft = torch.stft(
        audio,
        n_fft=400,
        hop_length=160,
        win_length=400,
        window=window,
        return_complex=True,
    )
    
    magnitude = torch.abs(stft)
    
    mel_filters = torch.from_numpy(
        librosa.filters.mel(sr=16000, n_fft=400, n_mels=n_mels)
    ).float()
    if device is not None:
        mel_filters = mel_filters.to(device)
    
    mel_spec = torch.matmul(mel_filters, magnitude)
    
    log_mel_spec = torch.log(torch.clamp(mel_spec, min=1e-9))
    
    return log_mel_spec