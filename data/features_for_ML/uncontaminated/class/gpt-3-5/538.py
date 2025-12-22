import os

class Document:

    def __init__(self):
        self.content = ""

    def document_analysis(self, document_path):
        self.read_document(document_path)
        # Perform analysis on the document content here
        print("Document analysis completed.")

    def read_document(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.content = file.read()
        else:
            print("File not found.")