import os
from pathlib import Path
from typing import Dict, List

def load_wordlist(data_dir: str) -> Dict[str, List[str]]:
    """
    Return a dictionary of wordlist with the following format:
        ke:
        ek:
    """
    result: Dict[str, List[str]] = {}
    base_path = Path(data_dir)

    for key in ("ke", "ek"):
        file_path = base_path / f"{key}.txt"
        words: List[str] = []

        if file_path.is_file():
            try:
                with file_path.open(encoding="utf-8") as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            words.append(word)
            except Exception:
                # If any error occurs while reading, keep the list empty
                words = []

        result[key] = words

    return result