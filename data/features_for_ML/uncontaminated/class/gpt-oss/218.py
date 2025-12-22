import os
import json
import re
from typing import List, Dict, Tuple

import nltk


class Utils:
    @staticmethod
    def sanitize_path(value: str) -> str:
        """
        Normalise a filesystem path:
        - Replace backslashes with forward slashes.
        - Collapse redundant separators.
        - Strip surrounding whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Path must be a string")
        # Strip whitespace
        path = value.strip()
        # Replace backslashes with forward slashes
        path = path.replace("\\", "/")
        # Normalise path (collapse redundant separators, resolve . and ..)
        path = os.path.normpath(path)
        # Convert back to forward slashes for consistency
        path = path.replace(os.sep, "/")
        return path

    @staticmethod
    def load_dataset(dataset_path: str) -> List[Dict]:
        """
        Load a JSON dataset from the given path.
        The file is expected to contain a JSON array of objects.
        """
        sanitized_path = Utils.sanitize_path(dataset_path)
        if not os.path.isfile(sanitized_path):
            raise FileNotFoundError(f"Dataset file not found: {sanitized_path}")
        with open(sanitized_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Dataset JSON must be a list of objects")
        # Ensure each item is a dict
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each dataset entry must be a JSON object (dict)")
        return data

    @staticmethod
    def split_prompt_template(asset: str) -> Tuple[str, str, List[str]]:
        """
        Split a prompt template into:
        - prefix: text before the first placeholder
        - suffix: text after the last placeholder
        - placeholders: list of placeholder names found in the template

        Placeholders are expected to be in the form {{placeholder}}.
        """
        if not isinstance(asset, str):
            raise TypeError("Asset must be a string")

        # Find all placeholders
        pattern = re.compile(r"\{\{(.*?)\}\}")
        placeholders = pattern.findall(asset)

        if not placeholders:
            # No placeholders: entire asset is both prefix and suffix
            return asset, "", []

        # Prefix: text before the first placeholder
        first_match = pattern.search(asset)
        prefix = asset[:first_match.start()] if first_match else ""

        # Suffix: text after the last placeholder
        last_match = pattern.search(asset)
        # Find last match
        for m in pattern.finditer(asset):
            last_match = m
        suffix = asset[last_match.end():] if last_match else ""

        return prefix, suffix, placeholders

    @staticmethod
    def download_required_nltk_resources():
        """
        Download the NLTK resources required for typical NLP tasks.
        """
        resources = [
            "punkt",
            "wordnet",
            "omw-1.4",
            "stopwords",
            "averaged_perceptron_tagger",
        ]
        for res in resources:
            nltk.download(res)