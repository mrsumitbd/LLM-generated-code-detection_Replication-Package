def split_into_sentences(text):
    sentences = []
    current_sentence = ''
    for char in text:
        if char in ['.', '!', '?']:
            sentences.append(current_sentence.strip())
            current_sentence = ''
        else:
            current_sentence += char
    if current_sentence:
        sentences.append(current_sentence.strip())
    return sentences