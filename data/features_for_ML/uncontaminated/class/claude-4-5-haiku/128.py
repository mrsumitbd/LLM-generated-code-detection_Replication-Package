class PreprocessorRegistry:
    _registry: dict[str, 'IPreprocessor'] = {}

    @staticmethod
    def register_preprocessor(preprocessor_id: str, preprocessor: 'IPreprocessor'):
        PreprocessorRegistry._registry[preprocessor_id] = preprocessor

    @staticmethod
    def get_preprocessor(preprocessor_id: str) -> 'IPreprocessor':
        return PreprocessorRegistry._registry.get(preprocessor_id)

    @staticmethod
    def get_preprocessor_ids() -> list[str]:
        return list(PreprocessorRegistry._registry.keys())