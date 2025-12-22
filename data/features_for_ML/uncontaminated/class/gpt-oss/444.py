import os
import json
from typing import List, Dict, Optional


class ChineseCangjieConverter:
    """Converts Chinese characters to Cangjie codes for tokenization."""

    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize the converter.

        Parameters
        ----------
        model_dir : str, optional
            Path to a directory containing a `cangjie_mapping.json` file.
            If not provided or the file is missing, a small built‑in mapping
            will be used.
        """
        self.model_dir = model_dir
        self.mapping: Dict[str, str] = self._load_cangjie_mapping(model_dir)
        self._init_segmenter()

    def _load_cangjie_mapping(self, model_dir: Optional[str] = None) -> Dict[str, str]:
        """
        Load the Cangjie mapping from a JSON file or fall back to a
        built‑in dictionary.

        Returns
        -------
        dict
            Mapping from a Chinese glyph to its Cangjie code.
        """
        mapping: Dict[str, str] = {}

        # Try to load from a file if a directory is provided
        if model_dir:
            mapping_path = os.path.join(model_dir, "cangjie_mapping.json")
            if os.path.isfile(mapping_path):
                try:
                    with open(mapping_path, "r", encoding="utf-8") as f:
                        mapping = json.load(f)
                except Exception:
                    # If loading fails, fall back to the default mapping
                    mapping = {}

        # Default minimal mapping if no file was loaded
        if not mapping:
            mapping = {
                "你": "U",
                "好": "H",
                "世": "S",
                "界": "J",
                "中": "Z",
                "国": "G",
                "人": "R",
                "的": "D",
                "我": "W",
                "爱": "A",
                "天": "T",
                "气": "Q",
                "很": "H",
                "吃": "C",
                "饭": "F",
                "吗": "M",
                "呀": "Y",
                "呀": "Y",
                "呀": "Y",
            }
        return mapping

    def _init_segmenter(self):
        """
        Initialize a segmenter.  For this lightweight implementation we
        simply treat each Chinese character as a token.  The method is kept
        for API compatibility with more advanced segmenters.
        """
        # No external segmenter is used; placeholder for future extensions.
        self.segmenter = None

    def _cangjie_encode(self, glyph: str) -> str:
        """
        Encode a single glyph to its Cangjie code.

        Parameters
        ----------
        glyph : str
            A single Chinese character.

        Returns
        -------
        str
            The Cangjie code if known, otherwise an empty string.
        """
        return self.mapping.get(glyph, "")

    def __call__(self, text: str) -> List[str]:
        """
        Convert a string of Chinese text into a list of Cangjie codes.

        Parameters
        ----------
        text : str
            Input text containing Chinese characters.

        Returns
        -------
        list of str
            Each element is either a Cangjie code or the original glyph
            if no code is available.
        """
        tokens: List[str] = []

        for ch in text:
            # Skip whitespace
            if ch.isspace():
                continue

            code = self._cangjie_encode(ch)
            if code:
                tokens.append(code)
            else:
                # If we don't have a mapping, keep the original glyph
                tokens.append(ch)

        return tokens