from typing import Optional

class GSVModel:
    pass

class ModelManager:

    def __init__(self):
        self.models = {}

    def load_cn_hubert(self) -> bool:
        # Implementation to load the CN Hubert model
        return True

    def get(self, character_name: str) -> Optional[GSVModel]:
        return self.models.get(character_name)

    def has_character(self, character_name: str) -> bool:
        return character_name in self.models

    def load_character(self, character_name: str, model_dir: str) -> bool:
        # Implementation to load a character model from the specified directory
        if character_name not in self.models:
            self.models[character_name] = GSVModel()
            return True
        return False

    def remove_character(self, character_name: str) -> None:
        if character_name in self.models:
            del self.models[character_name]

    def clean_cache(self) -> None:
        self.models = {}