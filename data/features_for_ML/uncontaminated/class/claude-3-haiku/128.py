class PreprocessorRegistry:
    _preprocessors = {}

    @staticmethod
    def register_preprocessor(preprocessor_id: str, preprocessor: 'IPreprocessor'):
        PreprocessorRegistry._preprocessors[preprocessor_id] = preprocessor

    @staticmethod
    def get_preprocessor(preprocessor_id: str) -> 'IPreprocessor':
        if preprocessor_id in PreprocessorRegistry._preprocessors:
            return PreprocessorRegistry._preprocessors[preprocessor_id]
        else:
            raise ValueError(f"Preprocessor with ID '{preprocessor_id}' not found.")

    @staticmethod
    def get_preprocessor_ids() -> list[str]:
        return list(PreprocessorRegistry._preprocessors.keys())