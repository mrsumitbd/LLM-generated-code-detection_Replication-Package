import os
import torch
import soundfile as sf

try:
    from TTS.api import TTS
except ImportError as e:
    raise ImportError(
        "The 'TTS' package is required for VuiTTS. "
        "Install it with: pip install TTS"
    ) from e


class VuiTTS:
    """
    A simple wrapper around the Coqui TTS library.

    Parameters
    ----------
    model_path : str
        Path to the TTS model checkpoint or a model identifier.
    device : str, optional
        Device to run the model on. Defaults to "cuda" if available,
        otherwise "cpu".
    """

    def __init__(self, model_path: str, device: str = "cuda"):
        self.model_path = model_path
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model = None

    def load_model(self):
        """
        Load the TTS model. This method is idempotent.
        """
        if self.model is None:
            self.model = TTS(self.model_path, device=self.device)

    def __call__(self, text: str, output_file: str = "output.wav"):
        """
        Synthesize speech from text and write to a WAV file.

        Parameters
        ----------
        text : str
            The input text to synthesize.
        output_file : str, optional
            Path to the output WAV file. Defaults to "output.wav".

        Returns
        -------
        str
            The path to the written WAV file.
        """
        if not text:
            raise ValueError("Input text must not be empty.")

        self.load_model()

        # Generate waveform (numpy array)
        wav = self.model.tts(text)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        # Write to file
        sf.write(output_file, wav, samplerate=self.model.synthesizer.synthesizer.sample_rate)

        return output_file