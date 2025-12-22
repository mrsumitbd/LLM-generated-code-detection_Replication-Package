import os
import torch
from typing import Optional, Tuple
from whisper import load_model, transcribe

def _prepare_cloning_inputs(
    clone_reference_filename: str,
    reference_audio_base_path: str,
    max_ref_duration_sec: float,
    whisper_model_name: str,
    whisper_cache_path: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[torch.Tensor], Optional[str]]:
    try:
        # Load the reference audio
        reference_audio_path = os.path.join(reference_audio_base_path, clone_reference_filename)
        audio_prompt_tensor = torch.load(reference_audio_path)

        # Check the duration of the reference audio
        if audio_prompt_tensor.shape[-1] / 16000 > max_ref_duration_sec:
            return None, "Reference audio duration exceeds the maximum allowed."

        # Get the transcript
        if transcript is None:
            # Use Whisper to transcribe the reference audio
            whisper_model = load_model(whisper_model_name, cache_dir=whisper_cache_path)
            result = transcribe(whisper_model, reference_audio_path)
            reference_transcript_text = result["text"]
        else:
            reference_transcript_text = transcript

        return audio_prompt_tensor, reference_transcript_text
    except Exception as e:
        return None, str(e)