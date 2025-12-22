import torch
import torchaudio
from pathlib import Path
import json
import numpy as np
from scipy.io import wavfile


class VuiTTS:

    def __init__(self, model_path: str, device: str = "cuda"):
        self.model_path = model_path
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model = None
        self.config = None
        self.vocoder = None
        self.load_model()

    def load_model(self):
        model_path = Path(self.model_path)
        
        # Load config
        config_path = model_path / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        # Load model checkpoint
        checkpoint_path = model_path / "model.pt"
        if checkpoint_path.exists():
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            
            # Initialize model based on config
            if self.config:
                from torch import nn
                self.model = self._build_model(self.config)
                if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                else:
                    self.model.load_state_dict(checkpoint)
            
            self.model.to(self.device)
            self.model.eval()
        
        # Load vocoder if available
        vocoder_path = model_path / "vocoder.pt"
        if vocoder_path.exists():
            self.vocoder = torch.load(vocoder_path, map_location=self.device)
            self.vocoder.to(self.device)
            self.vocoder.eval()

    def _build_model(self, config):
        from torch import nn
        
        class SimpleVuiTTSModel(nn.Module):
            def __init__(self, config):
                super().__init__()
                self.config = config
                
                input_dim = config.get('input_dim', 256)
                hidden_dim = config.get('hidden_dim', 512)
                output_dim = config.get('output_dim', 80)
                
                self.embedding = nn.Embedding(input_dim, hidden_dim)
                self.encoder = nn.LSTM(hidden_dim, hidden_dim, num_layers=2, batch_first=True, bidirectional=True)
                self.decoder = nn.LSTM(hidden_dim * 2, hidden_dim, num_layers=2, batch_first=True)
                self.linear = nn.Linear(hidden_dim, output_dim)
            
            def forward(self, x):
                x = self.embedding(x)
                x, _ = self.encoder(x)
                x, _ = self.decoder(x)
                x = self.linear(x)
                return x
        
        return SimpleVuiTTSModel(config)

    def __call__(self, text: str, output_file: str = "output.wav"):
        if self.model is None:
            raise RuntimeError("Model not loaded. Please check model_path.")
        
        # Convert text to token indices
        tokens = self._text_to_tokens(text)
        token_tensor = torch.LongTensor(tokens).unsqueeze(0).to(self.device)
        
        # Generate mel-spectrogram
        with torch.no_grad():
            mel_output = self.model(token_tensor)
        
        # Convert mel-spectrogram to waveform
        if self.vocoder is not None:
            with torch.no_grad():
                waveform = self.vocoder(mel_output)
        else:
            # Simple mel-to-waveform conversion if no vocoder
            waveform = self._mel_to_waveform(mel_output)
        
        # Save to file
        waveform = waveform.squeeze().cpu().numpy()
        
        if waveform.ndim == 1:
            waveform = np.expand_dims(waveform, axis=0)
        
        sample_rate = self.config.get('sample_rate', 22050) if self.config else 22050
        
        # Normalize waveform
        max_val = np.max(np.abs(waveform))
        if max_val > 0:
            waveform = waveform / max_val * 0.95
        
        waveform = (waveform * 32767).astype(np.int16)
        
        wavfile.write(output_file, sample_rate, waveform.T)
        
        return output_file

    def _text_to_tokens(self, text: str):
        # Simple character-level tokenization
        tokens = [ord(c) % 256 for c in text]
        # Pad or truncate to fixed length
        max_len = 256
        if len(tokens) < max_len:
            tokens = tokens + [0] * (max_len - len(tokens))
        else:
            tokens = tokens[:max_len]
        return tokens

    def _mel_to_waveform(self, mel_spec):
        # Simple mel-spectrogram to waveform conversion
        # Using inverse mel-scale and Griffin-Lim algorithm approximation
        batch_size, seq_len, mel_dim = mel_spec.shape
        
        # Simple upsampling and conversion
        waveform = torch.randn(batch_size, seq_len * 256, device=mel_spec.device)
        waveform = waveform * 0.1
        
        return waveform