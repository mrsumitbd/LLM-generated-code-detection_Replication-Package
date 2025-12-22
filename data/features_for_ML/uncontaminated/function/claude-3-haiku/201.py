def split_into_sentences(text):
    """Split the text into sentences.
    Args:
      text: A string that consists of more than or equal to one sentences.
    Returns:
      A list of strings where each string is a sentence.
    """
    sentences = text.split('.')
    return [sentence.strip() for sentence in sentences if sentence.strip()]