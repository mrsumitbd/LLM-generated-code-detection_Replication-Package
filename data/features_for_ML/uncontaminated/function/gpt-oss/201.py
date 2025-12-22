import re

def split_into_sentences(text):
    """Split the text into sentences.
    Args:
      text: A string that consists of more than or equal to one sentences.
    Returns:
      A list of strings where each string is a sentence.
    """
    if not text:
        return []

    # Regular expression to split on sentence-ending punctuation followed by whitespace.
    # It keeps the punctuation attached to the sentence.
    pattern = r'(?<=[.!?])\s+'
    parts = re.split(pattern, text.strip())

    # Filter out any empty strings that may arise from leading/trailing whitespace
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences