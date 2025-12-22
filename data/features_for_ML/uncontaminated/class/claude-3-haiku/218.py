import os
import json
from typing import List, Dict, Tuple
import nltk

class Utils:

    @staticmethod
    def sanitize_path(value: str) -> str:
        return os.path.normpath(value)

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict]:
        with open(Utils.sanitize_path(dataset_path), 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def split_prompt_template(asset: str) -> Tuple[str, str, List[str]]:
        prompt, response, keywords = asset.split('\n', 2)
        keywords = keywords.strip().split(', ')
        return prompt, response, keywords

    @staticmethod
    def download_required_nltk_resources():
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')