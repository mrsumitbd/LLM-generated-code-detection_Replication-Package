def split_text_for_tts(text: str, max_length: int = 4000) -> list[str]:
    """Split text into chunks that don't exceed the TTS API limit.

    The function splits text at sentence boundaries (periods, question marks, exclamation points)
    to create natural-sounding chunks. If a sentence is too long, it falls back to
    splitting at commas, then spaces.

    Args:
    ----
        text: The text to split.
        max_length: Maximum character length for each chunk (default 4000 to provide buffer).

    Returns:
    -------
        List of text chunks, each below the maximum length.

    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by sentence boundaries first
    sentences = []
    current_sentence = ""
    for char in text:
        current_sentence += char
        if char in '.!?':
            sentences.append(current_sentence)
            current_sentence = ""
    if current_sentence:
        sentences.append(current_sentence)
    
    for sentence in sentences:
        # If adding this sentence would exceed max_length
        if len(current_chunk) + len(sentence) > max_length:
            # If current chunk is not empty, save it
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # If the sentence itself is too long, split it further
            if len(sentence) > max_length:
                # Try splitting by commas
                parts = sentence.split(',')
                temp_chunk = ""
                for i, part in enumerate(parts):
                    part_with_comma = part + (',' if i < len(parts) - 1 else '')
                    
                    if len(temp_chunk) + len(part_with_comma) > max_length:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                            temp_chunk = ""
                        
                        # If part is still too long, split by spaces
                        if len(part_with_comma) > max_length:
                            words = part_with_comma.split()
                            word_chunk = ""
                            for word in words:
                                if len(word_chunk) + len(word) + 1 > max_length:
                                    if word_chunk:
                                        chunks.append(word_chunk.strip())
                                    word_chunk = word
                                else:
                                    word_chunk += (" " if word_chunk else "") + word
                            if word_chunk:
                                temp_chunk = word_chunk
                        else:
                            temp_chunk = part_with_comma
                    else:
                        temp_chunk += part_with_comma
                
                if temp_chunk:
                    current_chunk = temp_chunk
            else:
                current_chunk = sentence
        else:
            current_chunk += sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks