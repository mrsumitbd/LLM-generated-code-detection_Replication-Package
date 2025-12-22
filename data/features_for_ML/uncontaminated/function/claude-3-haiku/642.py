import re
from typing import Dict, Any
import spacy
from spacy.tokens import Doc

def extract_semantic_patterns(text: str) -> Dict[str, Any]:
    """
    Main entry point for extracting semantic patterns from code.
    Returns structured pattern data suitable for Qdrant metadata.
    """
    nlp = spacy.load("en_core_web_sm")
    doc: Doc = nlp(text)

    patterns = {
        "entities": extract_entities(doc),
        "noun_phrases": extract_noun_phrases(doc),
        "verb_phrases": extract_verb_phrases(doc),
        "adjective_phrases": extract_adjective_phrases(doc),
        "adverb_phrases": extract_adverb_phrases(doc),
        "prepositional_phrases": extract_prepositional_phrases(doc),
    }

    return patterns

def extract_entities(doc: Doc) -> Dict[str, Any]:
    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)
    return entities

def extract_noun_phrases(doc: Doc) -> List[str]:
    return [chunk.text for chunk in doc.noun_chunks]

def extract_verb_phrases(doc: Doc) -> List[str]:
    verb_phrases = []
    for token in doc:
        if token.pos_ == "VERB":
            verb_phrase = token.text
            for child in token.children:
                if child.pos_ in ["ADV", "ADP", "NOUN", "PRON"]:
                    verb_phrase += f" {child.text}"
            verb_phrases.append(verb_phrase)
    return verb_phrases

def extract_adjective_phrases(doc: Doc) -> List[str]:
    adjective_phrases = []
    for token in doc:
        if token.pos_ == "ADJ":
            adj_phrase = token.text
            for child in token.children:
                if child.pos_ in ["ADV"]:
                    adj_phrase = f"{child.text} {adj_phrase}"
            adjective_phrases.append(adj_phrase)
    return adjective_phrases

def extract_adverb_phrases(doc: Doc) -> List[str]:
    adverb_phrases = []
    for token in doc:
        if token.pos_ == "ADV":
            adv_phrase = token.text
            for child in token.children:
                if child.pos_ in ["ADV"]:
                    adv_phrase = f"{adv_phrase} {child.text}"
            adverb_phrases.append(adv_phrase)
    return adverb_phrases

def extract_prepositional_phrases(doc: Doc) -> List[str]:
    prepositional_phrases = []
    for token in doc:
        if token.pos_ == "ADP":
            prep_phrase = token.text
            for child in token.children:
                if child.pos_ in ["NOUN", "PRON"]:
                    prep_phrase += f" {child.text}"
            prepositional_phrases.append(prep_phrase)
    return prepositional_phrases