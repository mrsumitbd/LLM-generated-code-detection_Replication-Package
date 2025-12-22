class VuiTTS:

    def __init__(self, model_path: str, device: str = "cuda"):
        self.model_path = model_path
        self.device = device
        self.loaded_model = None

    def load_model(self):
        # Code to load the model
        self.loaded_model = True

    def __call__(self, text: str, output_file: str = "output.wav"):
        if self.loaded_model is None:
            self.load_model()
        
        # Code to generate speech from text and save to output_file
        print(f"Generated speech from '{text}' saved to '{output_file}'")