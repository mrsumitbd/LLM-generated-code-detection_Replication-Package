import os
import torch
import numpy as np
import torchaudio
from typing import Optional, Tuple, List, Dict, Any
from utils import (
    chunk_text_by_sentences,
    PerformanceMonitor,
    trim_lead_trail_silence,
    fix_internal_silence,
    remove_long_unvoiced_segments,
    _generate_transcript_with_whisper,  # Import Whisper helper
)

def _prepare_cloning_inputs(
    clone_reference_filename: str,
    reference_audio_base_path: str,
    max_ref_duration_sec: float,
    whisper_model_name: str,
    whisper_cache_path: str,
    transcript: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:  # MODIFIED return type
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
    global dia_model  # Need access to the loaded Dia model for DAC

    reference_audio_path = os.path.join(
        reference_audio_base_path, clone_reference_filename
    )
    if not os.path.isfile(reference_audio_path):
        return None, None, f"Reference audio file not found: {reference_audio_path}"

    # --- 1. Load and Process Audio (CPU only) ---
    try:
        logger.info(f"Loading reference audio: {reference_audio_path}")
        # Load on CPU without moving to device
        audio_tensor, sr = torchaudio.load(reference_audio_path)

        # Ensure correct sample rate
        if sr != EXPECTED_SAMPLE_RATE:
            logger.warning(
                f"Reference audio SR ({sr}Hz) differs from expected ({EXPECTED_SAMPLE_RATE}Hz). Resampling..."
            )
            resampled_tensor = torchaudio.functional.resample(
                audio_tensor, sr, EXPECTED_SAMPLE_RATE
            )
            del audio_tensor  # Free the original tensor
            audio_tensor = resampled_tensor

        # Ensure mono
        if audio_tensor.shape[0] > 1:
            logger.warning(
                f"Reference audio '{clone_reference_filename}' is stereo. Converting to mono."
            )
            mono_tensor = torch.mean(audio_tensor, dim=0, keepdim=True)
            del audio_tensor  # Free the stereo tensor
            audio_tensor = mono_tensor

        # Truncate if necessary
        num_samples = audio_tensor.shape[1]
        duration_sec = num_samples / EXPECTED_SAMPLE_RATE

        if duration_sec > max_ref_duration_sec:
            logger.warning(
                f"Reference audio duration ({duration_sec:.2f}s) exceeds max ({max_ref_duration_sec:.2f}s). Truncating..."
            )
            target_samples = int(max_ref_duration_sec * EXPECTED_SAMPLE_RATE)
            truncated_tensor = audio_tensor[:, :target_samples].clone()
            del audio_tensor  # Free the full audio tensor
            audio_tensor = truncated_tensor
            new_duration = audio_tensor.shape[1] / EXPECTED_SAMPLE_RATE
            logger.info(f"Truncated reference audio to {new_duration:.2f}s.")
        else:
            logger.info(
                f"Reference audio duration ({duration_sec:.2f}s) is within limit."
            )

        # Convert processed tensor to NumPy array (float32) for potential Whisper use
        processed_audio_np = audio_tensor.squeeze(0).numpy().astype(np.float32)

        # Clear tensors when done with them
        del audio_tensor

    except Exception as e:
        logger.error(
            f"Error loading/processing reference audio '{reference_audio_path}': {e}",
            exc_info=True,
        )
        return None, None, f"Failed to load/process reference audio: {e}"

    # --- 2. Get Transcript ---
    transcript_text: Optional[str] = None
    error_message: Optional[str] = None
    transcript_source: str = "unknown"

    if transcript is not None:
        logger.info("Using provided transcript override for cloning.")
        transcript_text = transcript.strip()
        transcript_source = "explicit"
        # Check and prepend [S1] or [S2] if needed (assuming clone target is usually S1)
        if not transcript_text.startswith(("[S1]", "[S2]")):
            logger.debug("Prepending '[S1] ' to explicit transcript.")
            transcript_text = "[S1] " + transcript_text

    else:
        # Try loading local .txt file
        base_name, _ = os.path.splitext(clone_reference_filename)
        transcript_filename = base_name + ".txt"
        transcript_filepath = os.path.join(
            reference_audio_base_path, transcript_filename
        )
        logger.info(f"Checking for local transcript: {transcript_filepath}")

        if os.path.isfile(transcript_filepath):
            try:
                with open(transcript_filepath, "r", encoding="utf-8") as f:
                    transcript_text = f.read().strip()
                logger.info(f"Loaded transcript from local file: {transcript_filepath}")
                transcript_source = "file"
                # Assume file is correctly formatted (includes speaker tags)
                # Ensure tag exists just in case file is malformed
                if not transcript_text.startswith(("[S1]", "[S2]")):
                    logger.warning(
                        f"Local transcript file '{transcript_filepath}' missing speaker tag. Prepending '[S1]'."
                    )
                    transcript_text = "[S1] " + transcript_text
            except Exception as e:
                logger.warning(
                    f"Failed to read local transcript file '{transcript_filepath}': {e}. Will attempt Whisper.",
                    exc_info=True,
                )
                transcript_text = None  # Ensure it's None so Whisper runs

        if transcript_text is None:
            # Try Whisper
            logger.info(
                "Local transcript not found or failed to load. Attempting Whisper generation..."
            )
            generated_transcript = _generate_transcript_with_whisper(
                processed_audio_np, whisper_model_name, whisper_cache_path
            )

            if generated_transcript is not None:
                transcript_text = "[S1] " + generated_transcript.strip()  # Prepend [S1]
                transcript_source = "whisper"
                logger.info("Whisper transcription successful.")
                # Save the generated transcript
                try:
                    with open(transcript_filepath, "w", encoding="utf-8") as f:
                        f.write(transcript_text)  # Save with the [S1] tag
                    logger.info(f"Saved Whisper transcript to: {transcript_filepath}")
                except Exception as e:
                    logger.warning(
                        f"Failed to save generated transcript to '{transcript_filepath}': {e}",
                        exc_info=True,
                    )
            else:
                logger.error("Whisper transcription failed.")
                error_message = "Reference transcript file not found and automatic transcription failed."
                transcript_source = "failed"

    # --- 3. Check if Transcript was Obtained ---
    if transcript_text is None:
        # Free resources before returning
        del processed_audio_np
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return None, None, error_message or "Failed to obtain reference transcript."

    # Free resources before returning
    del processed_audio_np
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Return without audio_prompt_tensor (step 4 deleted)
    return None, transcript_text, None