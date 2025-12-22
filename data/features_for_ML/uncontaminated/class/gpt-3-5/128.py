from typing import Dict, List

class PreprocessorRegistry:
    _preprocessors: Dict[str, IPreprocessor] = {}

    @staticmethod
    def register_preprocessor(preprocessor_id: str, preprocessor: IPreprocessor):
        PreprocessorRegistry._preprocessors[preprocessor_id] = preprocessor

    @staticmethod
    def get_preprocessor(preprocessor_id: str) -> IPreprocessor:
        return PreprocessorRegistry._preprocessors.get(preprocessor_id)

    @staticmethod
    def get_preprocessor_ids() -> List[str]:
        return list(PreprocessorRegistry._preprocessors.keys())