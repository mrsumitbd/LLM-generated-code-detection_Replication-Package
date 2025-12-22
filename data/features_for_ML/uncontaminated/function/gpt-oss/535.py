import os
from typing import Optional, Tuple

import torch
import torchaudio
import whisper


def _prepare_cloning_inputs(
    clone_reference_filename: str,
    reference_audio_base_path: str,
    max_ref_duration_sec: float,
    whisper_model_name: str,
    whisper_cache_path: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[torch.Tensor], Optional[str], Optional[str]]:
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
    try:
        # Build full path to the reference audio file
        audio_path = os.path.join(reference_audio_base_path, clone_reference_filename)
        if not os.path.isfile(audio_path):
            return None, None, f"Reference audio file not found: {audio_path}"

        # Load audio
        waveform, sample_rate = torchaudio.load(audio_path)  # waveform shape: (channels, samples)

        # Resample to 16kHz if needed
        target_sr = 16000
        if sample_rate != target_sr:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sr)
            waveform = resampler(waveform)
            sample_rate = target_sr

        # Convert to mono by averaging channels if necessary
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Trim to maximum duration if specified
        if max_ref_duration_sec is not None:
            max_samples = int(max_ref_duration_sec * sample_rate)
            if waveform.shape[1] > max_samples:
                waveform = waveform[:, :max_samples]

        # Get transcript
        if transcript is not None:
            transcript_text = transcript.strip()
        else:
            # Try to read a .txt file with the same base name
            txt_path = os.path.splitext(audio_path)[0] + ".txt"
            if os.path.isfile(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    transcript_text = f.read().strip()
            else:
                # Fallback to Whisper transcription
                model = whisper.load_model(
                    whisper_model_name,
                    download_root=whisper_cache_path,
                )
                result = model.transcribe(audio_path)
                transcript_text = result.get("text", "").strip()

        return waveform, transcript_text, None

    except Exception as exc:
        # On any error, return None for data and the error message
        return None, None, str(exc)