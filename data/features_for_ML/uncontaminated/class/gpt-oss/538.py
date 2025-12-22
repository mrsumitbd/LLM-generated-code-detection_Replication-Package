class Document:
    def __init__(self):
        self.content = ""

    def read_document(self, file_path):
        """
        Reads the content of a text file and stores it in the instance.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.content = f.read()
            return self.content
        except Exception as e:
            raise RuntimeError(f"Failed to read document: {e}")

    def document_analysis(self, document_path):
        """
        Performs a simple analysis on the document:
        - number of lines
        - number of words
        - number of characters
        - number of unique words
        - most common word and its count
        """
        content = self.read_document(document_path)

        lines = content.splitlines()
        words = content.split()
        num_lines = len(lines)
        num_words = len(words)
        num_chars = len(content)
        unique_words = set(words)
        num_unique = len(unique_words)

        from collections import Counter
        counter = Counter(words)
        most_common = counter.most_common(1)[0] if counter else (None, 0)

        return {
            "lines": num_lines,
            "words": num_words,
            "characters": num_chars,
            "unique_words": num_unique,
            "most_common_word": most_common[0],
            "most_common_word_count": most_common[1],
        }