from typing import List, Dict, Tuple

class Utils:

    @staticmethod
    def sanitize_path(value: str) -> str:
        sanitized_value = value.replace('\\', '/').strip()
        if sanitized_value.endswith('/'):
            sanitized_value = sanitized_value[:-1]
        return sanitized_value

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict]:
        dataset = []
        # Load dataset from the specified path
        return dataset

    @staticmethod
    def split_prompt_template(asset: str) -> Tuple[str, str, List[str]]:
        parts = asset.split('|')
        if len(parts) == 3:
            return parts[0], parts[1], parts[2].split(',')
        else:
            return '', '', []

    @staticmethod
    def download_required_nltk_resources():
        import nltk
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')