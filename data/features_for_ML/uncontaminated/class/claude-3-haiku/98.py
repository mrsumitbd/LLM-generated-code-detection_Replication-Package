from typing import Optional
from .gsv_model import GSVModel

class ModelManager:
    def __init__(self):
        self.models = {}
        self.cn_hubert_loaded = False

    def load_cn_hubert(self) -> bool:
        if not self.cn_hubert_loaded:
            # Load the CN Hubert model
            self.cn_hubert_loaded = True
            return True
        return False

    def get(self, character_name: str) -> Optional[GSVModel]:
        if character_name in self.models:
            return self.models[character_name]
        return None

    def has_character(self, character_name: str) -> bool:
        return character_name in self.models

    def load_character(self, character_name: str, model_dir: str) -> bool:
        if character_name not in self.models:
            # Load the character model from the specified directory
            self.models[character_name] = GSVModel(model_dir)
            return True
        return False

    def remove_character(self, character_name: str) -> None:
        if character_name in self.models:
            del self.models[character_name]

    def clean_cache(self) -> None:
        self.models.clear()
        self.cn_hubert_loaded = False