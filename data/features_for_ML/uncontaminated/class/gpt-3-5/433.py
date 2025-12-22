from typing import List, Dict
import numpy as np

class PDFExtractor:

    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        pass

    def chunk_text(self, pages: List[str], max_chunk_size: int = 500) -> List[str]:
        pass

    def embed_text(self, text: str) -> np.ndarray:
        pass

    def store_embeddings(self, pdf_id: str, chunks: List[str]) -> List[str]:
        pass

    def query_embeddings(self, pdf_id: str, query_text: str, top_k: int = 3) -> List[Dict]:
        pass

    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        pass

    def delete_vectors_by_pdf_id(self, pdf_id: str):
        pass

    def start_gradio(self):
        pass

    def run_cli(self):
        pass