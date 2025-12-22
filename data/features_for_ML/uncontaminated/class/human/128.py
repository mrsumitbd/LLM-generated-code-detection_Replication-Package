from .interface import IPreprocessor

class PreprocessorRegistry:
    _preprocessor_registry: dict[str, type[IPreprocessor]] = {}

    @staticmethod
    def register_preprocessor(preprocessor_id: str, preprocessor: IPreprocessor):
        PreprocessorRegistry._preprocessor_registry[preprocessor_id] = preprocessor

    @staticmethod
    def get_preprocessor(preprocessor_id: str) -> IPreprocessor:
        return PreprocessorRegistry._preprocessor_registry[preprocessor_id]

    @staticmethod
    def get_preprocessor_ids() -> list[str]:
        return list(PreprocessorRegistry._preprocessor_registry.keys())