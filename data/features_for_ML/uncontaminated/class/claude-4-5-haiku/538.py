import os
import re
from collections import Counter
from pathlib import Path

class Document:

    def __init__(self):
        self.content = None
        self.file_path = None
        self.word_count = 0
        self.sentence_count = 0
        self.paragraph_count = 0
        self.unique_words = 0
        self.average_word_length = 0.0
        self.character_count = 0

    def document_analysis(self, document_path):
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        self.read_document(document_path)
        
        if not self.content:
            return {
                'file_path': document_path,
                'word_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'unique_words': 0,
                'average_word_length': 0.0,
                'character_count': 0
            }
        
        # Count characters (excluding whitespace)
        self.character_count = len(self.content.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        # Count paragraphs
        self.paragraph_count = len([p for p in self.content.split('\n\n') if p.strip()])
        
        # Count sentences
        sentences = re.split(r'[.!?]+', self.content)
        self.sentence_count = len([s for s in sentences if s.strip()])
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]+\b', self.content.lower())
        self.word_count = len(words)
        self.unique_words = len(set(words))
        
        # Calculate average word length
        if self.word_count > 0:
            self.average_word_length = sum(len(word) for word in words) / self.word_count
        else:
            self.average_word_length = 0.0
        
        return {
            'file_path': document_path,
            'word_count': self.word_count,
            'sentence_count': self.sentence_count,
            'paragraph_count': self.paragraph_count,
            'unique_words': self.unique_words,
            'average_word_length': round(self.average_word_length, 2),
            'character_count': self.character_count
        }

    def read_document(self, file_path):
        self.file_path = file_path
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                self.content = file.read()
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
        
        return self.content