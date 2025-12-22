import os
import uuid
import argparse
import json
from typing import List, Dict, Tuple

import numpy as np
import gradio as gr
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Optional: OpenAI for answer generation
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class PDFExtractor:
    """
    A simple PDF text extractor, chunker, embedder, and retriever.
    """

    def __init__(self):
        # In‑memory vector store: {pdf_id: List[Tuple[chunk, embedding]]}
        self.vector_store: Dict[str, List[Tuple[str, np.ndarray]]] = {}
        # Load a default sentence transformer model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # ------------------------------------------------------------------
    # PDF extraction
    # ------------------------------------------------------------------
    def extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        """
        Extracts text from each page of a PDF file.

        :param pdf_path: Path to the PDF file.
        :return: List of page texts.
        """
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        reader = PdfReader(pdf_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text.strip())
        return pages

    # ------------------------------------------------------------------
    # Text chunking
    # ------------------------------------------------------------------
    def chunk_text(self, pages: List[str], max_chunk_size: int = 500) -> List[str]:
        """
        Splits page texts into smaller chunks.

        :param pages: List of page texts.
        :param max_chunk_size: Maximum number of characters per chunk.
        :return: List of text chunks.
        """
        chunks = []
        for page in pages:
            start = 0
            while start < len(page):
                end = min(start + max_chunk_size, len(page))
                chunk = page[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start = end
        return chunks

    # ------------------------------------------------------------------
    # Embedding
    # ------------------------------------------------------------------
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generates an embedding vector for a given text.

        :param text: Input text.
        :return: Embedding vector as a NumPy array.
        """
        return self.model.encode(text, convert_to_numpy=True)

    # ------------------------------------------------------------------
    # Store embeddings
    # ------------------------------------------------------------------
    def store_embeddings(self, pdf_id: str, chunks: List[str]) -> List[str]:
        """
        Stores embeddings for each chunk under a PDF ID.

        :param pdf_id: Unique identifier for the PDF.
        :param chunks: List of text chunks.
        :return: List of chunk IDs (UUIDs).
        """
        embeddings = []
        chunk_ids = []
        for chunk in chunks:
            emb = self.embed_text(chunk)
            embeddings.append((chunk, emb))
            chunk_ids.append(str(uuid.uuid4()))
        self.vector_store[pdf_id] = embeddings
        return chunk_ids

    # ------------------------------------------------------------------
    # Query embeddings
    # ------------------------------------------------------------------
    def query_embeddings(self, pdf_id: str, query_text: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieves the top_k most similar chunks for a query.

        :param pdf_id: PDF ID to search in.
        :param query_text: Query string.
        :param top_k: Number of results to return.
        :return: List of dicts with 'chunk' and 'score'.
        """
        if pdf_id not in self.vector_store:
            raise KeyError(f"No embeddings found for PDF ID: {pdf_id}")

        query_emb = self.embed_text(query_text).reshape(1, -1)
        results = []
        for chunk, emb in self.vector_store[pdf_id]:
            score = float(cosine_similarity(query_emb, emb.reshape(1, -1))[0][0])
            results.append({"chunk": chunk, "score": score})

        # Sort by similarity score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Generate answer
    # ------------------------------------------------------------------
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Generates an answer to a question given context chunks.

        :param question: The user's question.
        :param context_chunks: List of relevant text chunks.
        :return: Generated answer string.
        """
        context = "\n\n".join(context_chunks)
        prompt = (
            f"You are a helpful assistant. Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\nAnswer:"
        )

        if OPENAI_AVAILABLE:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=256,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                # Fallback to simple summarization if OpenAI fails
                pass

        # Simple fallback: return the first context chunk or a placeholder
        if context_chunks:
            return f"Answer based on context: {context_chunks[0][:200]}..."
        return "Sorry, I couldn't generate an answer."

    # ------------------------------------------------------------------
    # Delete vectors
    # ------------------------------------------------------------------
    def delete_vectors_by_pdf_id(self, pdf_id: str):
        """
        Deletes all stored embeddings for a given PDF ID.

        :param pdf_id: PDF ID to delete.
        """
        if pdf_id in self.vector_store:
            del self.vector_store[pdf_id]

    # ------------------------------------------------------------------
    # Gradio UI
    # ------------------------------------------------------------------
    def start_gradio(self):
        """
        Starts a Gradio web interface for uploading PDFs, asking questions,
        and displaying answers.
        """

        def process_pdf(pdf_file, question):
            if pdf_file is None:
                return "Please upload a PDF file.", ""
            pdf_path = pdf_file.name
            pdf_id = str(uuid.uuid4())
            pages = self.extract_text_from_pdf(pdf_path)
            chunks = self.chunk_text(pages)
            self.store_embeddings(pdf_id, chunks)
            results = self.query_embeddings(pdf_id, question, top_k=3)
            context_chunks = [r["chunk"] for r in results]
            answer = self.generate_answer(question, context_chunks)
            return f"Top {len(results)} chunks retrieved.", answer

        with gr.Blocks() as demo:
            gr.Markdown("# PDF Question‑Answer System")
            pdf_input = gr.File(label="Upload PDF")
            question_input = gr.Textbox(label="Your Question", lines=2)
            submit_btn = gr.Button("Ask")
            status_output = gr.Textbox(label="Status")
            answer_output = gr.Textbox(label="Answer", lines=5)

            submit_btn.click(
                fn=process_pdf,
                inputs=[pdf_input, question_input],
                outputs=[status_output, answer_output],
            )

        demo.launch()

    # ------------------------------------------------------------------
    # CLI
    # ------------------------------------------------------------------
    def run_cli(self):
        """
        Runs a simple command‑line interface for extracting, querying,
        and deleting PDFs.
        """
        parser = argparse.ArgumentParser(description="PDF Extractor CLI")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Extract command
        extract_parser = subparsers.add_parser("extract", help="Extract and store PDF embeddings")
        extract_parser.add_argument("pdf_path", help="Path to the PDF file")

        # Query command
        query_parser = subparsers.add_parser("query", help="Query a stored PDF")
        query_parser.add_argument("pdf_id", help="PDF ID to query")
        query_parser.add_argument("question", help="Question to ask")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete embeddings by PDF ID")
        delete_parser.add_argument("pdf_id", help="PDF ID to delete")

        args = parser.parse_args()

        if args.command == "extract":
            pages = self.extract_text_from_pdf(args.pdf_path)
            chunks = self.chunk_text(pages)
            pdf_id = str(uuid.uuid4())
            self.store_embeddings(pdf_id, chunks)
            print(f"PDF processed. ID: {pdf_id}")

        elif args.command == "query":
            results = self.query_embeddings(args.pdf_id, args.question, top_k=3)
            context_chunks = [r["chunk"] for r in results]
            answer = self.generate_answer(args.question, context_chunks)
            print("Answer:")
            print(answer)

        elif args.command == "delete":
            self.delete_vectors_by_pdf_id(args.pdf_id)
            print(f"Deleted embeddings for PDF ID: {args.pdf_id}")