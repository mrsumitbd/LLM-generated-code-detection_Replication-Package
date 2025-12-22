class ModelManager:
    def __init__(self):
        self._models = {}
        self._cn_hubert = None
        self._cn_hubert_loaded = False

    def load_cn_hubert(self) -> bool:
        try:
            if self._cn_hubert_loaded:
                return True
            # Placeholder for actual cn_hubert loading logic
            self._cn_hubert = True
            self._cn_hubert_loaded = True
            return True
        except Exception:
            return False

    def get(self, character_name: str) -> Optional['GSVModel']:
        return self._models.get(character_name)

    def has_character(self, character_name: str) -> bool:
        return character_name in self._models

    def load_character(self, character_name: str, model_dir: str) -> bool:
        try:
            if character_name in self._models:
                return True
            # Placeholder for actual model loading logic
            model = GSVModel()
            self._models[character_name] = model
            return True
        except Exception:
            return False

    def remove_character(self, character_name: str) -> None:
        if character_name in self._models:
            del self._models[character_name]

    def clean_cache(self) -> None:
        self._models.clear()
        self._cn_hubert = None
        self._cn_hubert_loaded = False