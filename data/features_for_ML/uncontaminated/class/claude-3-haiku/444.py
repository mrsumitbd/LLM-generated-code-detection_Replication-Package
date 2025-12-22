import os
import json
from typing import List

class ChineseCangjieConverter:
    """Converts Chinese characters to Cangjie codes for tokenization."""

    def __init__(self, model_dir=None):
        self.cangjie_mapping = self._load_cangjie_mapping(model_dir)
        self.segmenter = self._init_segmenter()

    def _load_cangjie_mapping(self, model_dir=None):
        if model_dir is None:
            model_dir = os.path.dirname(__file__)
        mapping_file = os.path.join(model_dir, 'cangjie_mapping.json')
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _init_segmenter(self):
        # Initialize a Chinese text segmenter
        # (implementation not provided in the given skeleton)
        pass

    def _cangjie_encode(self, glyph: str):
        if glyph in self.cangjie_mapping:
            return self.cangjie_mapping[glyph]
        else:
            return None

    def __call__(self, text):
        tokens = self.segmenter.segment(text)
        cangjie_codes = [self._cangjie_encode(token) for token in tokens]
        return [code for code in cangjie_codes if code is not None]