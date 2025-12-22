import os
import shutil
from typing import Optional, Dict

# Minimal placeholder for GSVModel
class GSVModel:
    def __init__(self, path: str):
        self.path = path
        # In a real implementation, load the model files here
        # e.g., self.model = torch.load(os.path.join(path, "model.pt"))

    def __repr__(self):
        return f"<GSVModel path={self.path!r}>"

class ModelManager:
    def __init__(self):
        # Dictionary to store loaded character models
        self._models: Dict[str, GSVModel] = {}
        # Placeholder for the Chinese HuBERT model
        self._hubert = None
        # Cache directory for downloaded models
        self._cache_dir = os.path.abspath("./model_cache")
        os.makedirs(self._cache_dir, exist_ok=True)

    def load_cn_hubert(self) -> bool:
        """
        Load the Chinese HuBERT model from Hugging Face.
        Returns True if successful, False otherwise.
        """
        try:
            from transformers import AutoModel
            # Use a pretrained HuBERT model
            self._hubert = AutoModel.from_pretrained(
                "facebook/hubert-large-ls960-ft",
                cache_dir=self._cache_dir,
            )
            return True
        except Exception:
            self._hubert = None
            return False

    def get(self, character_name: str) -> Optional[GSVModel]:
        """
        Retrieve the GSVModel for the given character name.
        """
        return self._models.get(character_name)

    def has_character(self, character_name: str) -> bool:
        """
        Check if a model for the given character name is loaded.
        """
        return character_name in self._models

    def load_character(self, character_name: str, model_dir: str) -> bool:
        """
        Load a character model from the specified directory.
        The model directory is copied into the cache directory.
        """
        if not os.path.isdir(model_dir):
            return False

        # Copy the model directory into the cache
        dest_dir = os.path.join(self._cache_dir, character_name)
        try:
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(model_dir, dest_dir)
            # Instantiate the GSVModel
            self._models[character_name] = GSVModel(dest_dir)
            return True
        except Exception:
            return False

    def remove_character(self, character_name: str) -> None:
        """
        Remove the loaded model for the given character name.
        """
        if character_name in self._models:
            # Remove from memory
            del self._models[character_name]
            # Remove from cache directory
            cache_path = os.path.join(self._cache_dir, character_name)
            if os.path.isdir(cache_path):
                shutil.rmtree(cache_path)

    def clean_cache(self) -> None:
        """
        Clean the entire cache directory and unload all models.
        """
        # Remove all cached model directories
        for entry in os.listdir(self._cache_dir):
            path = os.path.join(self._cache_dir, entry)
            if os.path.isdir(path):
                shutil.rmtree(path)
        # Clear the in-memory model dictionary
        self._models.clear()