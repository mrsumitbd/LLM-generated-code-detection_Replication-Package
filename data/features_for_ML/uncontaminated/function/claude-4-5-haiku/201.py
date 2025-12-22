import re
from anthropic import Anthropic

def split_into_sentences(text):
    """Split the text into sentences.
    Args:
      text: A string that consists of more than or equal to one sentences.
    Returns:
      A list of strings where each string is a sentence.
    """
    client = Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Split the following text into sentences. Return ONLY a Python list of strings, where each string is a sentence. Do not include any explanation or additional text.

Text: {text}

Return format: ["sentence1", "sentence2", "sentence3", ...]"""
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    try:
        sentences = eval(response_text)
        if isinstance(sentences, list):
            return sentences
    except:
        pass
    
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]