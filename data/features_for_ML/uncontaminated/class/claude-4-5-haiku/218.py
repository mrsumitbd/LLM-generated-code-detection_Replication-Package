import os
import json
import re
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Utils:

    @staticmethod
    def sanitize_path(value: str) -> str:
        """Sanitize file path by removing/replacing invalid characters."""
        # Remove leading/trailing whitespace
        value = value.strip()
        # Replace backslashes with forward slashes
        value = value.replace('\\', '/')
        # Remove any null characters
        value = value.replace('\x00', '')
        # Remove any control characters
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\t\n\r')
        return value

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict]:
        """Load dataset from JSON file."""
        sanitized_path = Utils.sanitize_path(dataset_path)
        
        if not os.path.exists(sanitized_path):
            raise FileNotFoundError(f"Dataset file not found: {sanitized_path}")
        
        try:
            with open(sanitized_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ValueError("Dataset must be a JSON object or array")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in dataset file: {e}")

    @staticmethod
    def split_prompt_template(asset: str) -> Tuple[str, str, List[str]]:
        """
        Split prompt template into system prompt, user prompt, and variables.
        Expected format: {{system_prompt}}{{user_prompt}}{{var1}}{{var2}}...
        """
        # Find all variables in format {{variable_name}}
        variable_pattern = r'\{\{([^}]+)\}\}'
        variables = re.findall(variable_pattern, asset)
        
        # Split by first occurrence of {{ to separate system and user prompts
        parts = asset.split('{{', 1)
        
        if len(parts) < 2:
            return asset, "", []
        
        system_prompt = parts[0].strip()
        remaining = '{{' + parts[1]
        
        # Extract first variable (user prompt marker)
        first_var_match = re.search(variable_pattern, remaining)
        if not first_var_match:
            return system_prompt, remaining, []
        
        user_prompt_end = first_var_match.start()
        user_prompt = remaining[:user_prompt_end].strip()
        
        # Remove system and user prompt from variables list if they're there
        filtered_variables = [v for v in variables if v not in ['system_prompt', 'user_prompt']]
        
        return system_prompt, user_prompt, filtered_variables

    @staticmethod
    def download_required_nltk_resources():
        """Download required NLTK resources."""
        required_resources = [
            'punkt',
            'stopwords',
            'averaged_perceptron_tagger',
            'maxent_ne_chunker',
            'words'
        ]
        
        for resource in required_resources:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Warning: Could not download NLTK resource '{resource}': {e}")