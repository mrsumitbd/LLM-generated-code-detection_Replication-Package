import os
import re

class Document:
    def __init__(self):
        self.word_count = 0
        self.unique_words = set()
        self.word_frequency = {}

    def document_analysis(self, document_path):
        self.read_document(document_path)
        self.analyze_document()

    def read_document(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.text = file.read()
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def analyze_document(self):
        words = re.findall(r'\w+', self.text.lower())
        self.word_count = len(words)
        self.unique_words = set(words)

        for word in words:
            if word in self.word_frequency:
                self.word_frequency[word] += 1
            else:
                self.word_frequency[word] = 1