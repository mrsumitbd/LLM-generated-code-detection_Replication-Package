import re
import spacy

def task_knowledge_extraction():
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Define the input text
    text = "The quick brown fox jumps over the lazy dog. This is a sample text for knowledge extraction."

    # Process the text using the spaCy pipeline
    doc = nlp(text)

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Extract noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    # Extract keywords using a simple frequency-based approach
    word_freq = {}
    for token in doc:
        if not token.is_stop and not token.is_punct:
            word_freq[token.text] = word_freq.get(token.text, 0) + 1
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]

    # Return the extracted knowledge
    return {
        "entities": entities,
        "noun_phrases": noun_phrases,
        "keywords": keywords
    }