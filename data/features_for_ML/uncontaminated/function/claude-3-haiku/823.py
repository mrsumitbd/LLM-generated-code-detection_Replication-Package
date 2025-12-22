import re
from collections import Counter
from typing import List, Dict

def build_search_index(messages: List[Dict], patterns: List[Dict], errors: List[Dict]) -> str:
    """
    Build 500-token search index optimized for keyword matching.

    Opus structure:
    - User request (exact words)
    - Solution type + tools used
    - Files modified + operation types
    - Primary keywords (3-5 specific terms)
    """
    # Combine all messages, patterns, and errors into a single list of text
    all_text = [msg['text'] for msg in messages] + [p['pattern'] for p in patterns] + [e['error'] for e in errors]

    # Extract all unique words from the combined text
    all_words = set(' '.join(all_text).lower().split())

    # Count the frequency of each word
    word_counts = Counter(' '.join(all_text).lower().split())

    # Sort the words by frequency and select the top 500 words
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_500_words = [word for word, _ in sorted_words[:500]]

    # Build the search index as a string
    search_index = ' '.join(top_500_words)
    return search_index