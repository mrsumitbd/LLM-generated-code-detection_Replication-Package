import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class VuiTTS:
    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = torch.device(device)
        self.processor = Wav2Vec2Processor.from_pretrained(model_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_path).to(self.device)

    def load_model(self):
        pass

    def __call__(self, text: str, output_file: str = "output.wav"):
        input_ids = self.processor(text, return_tensors="pt", padding=True).input_ids
        input_ids = input_ids.to(self.device)
        output = self.model(input_ids).logits
        predicted_ids = torch.argmax(output, dim=-1)
        predicted_text = self.processor.decode(predicted_ids[0], skip_special_tokens=True)
        # Save the generated audio to the output file
        self.processor.save_pretrained(predicted_text, output_file)