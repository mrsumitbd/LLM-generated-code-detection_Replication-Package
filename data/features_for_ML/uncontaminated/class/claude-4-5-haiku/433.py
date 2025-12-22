from typing import List, Dict
import numpy as np
import PyPDF2
from sentence_transformers import SentenceTransformer
import gradio as gr
from pinecone import Pinecone
import os
from anthropic import Anthropic

class PDFExtractor:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index = self.pc.Index('pdf-embeddings')
        self.client = Anthropic()
        self.conversation_history = []

    def extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        pages = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                pages.append(text)
        return pages

    def chunk_text(self, pages: List[str], max_chunk_size: int = 500) -> List[str]:
        chunks = []
        for page in pages:
            words = page.split()
            current_chunk = []
            current_size = 0
            
            for word in words:
                word_size = len(word) + 1
                if current_size + word_size > max_chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_size = word_size
                else:
                    current_chunk.append(word)
                    current_size += word_size
            
            if current_chunk:
                chunks.append(' '.join(current_chunk))
        
        return chunks

    def embed_text(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text)
        return embedding

    def store_embeddings(self, pdf_id: str, chunks: List[str]) -> List[str]:
        chunk_ids = []
        vectors = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{pdf_id}_chunk_{i}"
            embedding = self.embed_text(chunk)
            vectors.append((chunk_id, embedding.tolist(), {"text": chunk, "pdf_id": pdf_id}))
            chunk_ids.append(chunk_id)
        
        self.index.upsert(vectors=vectors)
        return chunk_ids

    def query_embeddings(self, pdf_id: str, query_text: str, top_k: int = 3) -> List[Dict]:
        query_embedding = self.embed_text(query_text)
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            filter={"pdf_id": {"$eq": pdf_id}},
            include_metadata=True
        )
        
        context_chunks = []
        for match in results['matches']:
            context_chunks.append({
                'id': match['id'],
                'text': match['metadata']['text'],
                'score': match['score']
            })
        
        return context_chunks

    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        context = "\n".join(context_chunks)
        
        self.conversation_history.append({
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a helpful assistant that answers questions based on provided context. Answer concisely and accurately.",
            messages=self.conversation_history
        )
        
        answer = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": answer
        })
        
        return answer

    def delete_vectors_by_pdf_id(self, pdf_id: str):
        self.index.delete(filter={"pdf_id": {"$eq": pdf_id}})

    def start_gradio(self):
        def process_pdf_and_query(pdf_file, query):
            if pdf_file is None:
                return "Please upload a PDF file"
            
            pdf_path = pdf_file.name
            pdf_id = os.path.basename(pdf_path).replace('.pdf', '')
            
            pages = self.extract_text_from_pdf(pdf_path)
            chunks = self.chunk_text(pages)
            self.store_embeddings(pdf_id, chunks)
            
            context_results = self.query_embeddings(pdf_id, query)
            context_chunks = [result['text'] for result in context_results]
            
            answer = self.generate_answer(query, context_chunks)
            
            self.delete_vectors_by_pdf_id(pdf_id)
            
            return answer
        
        interface = gr.Interface(
            fn=process_pdf_and_query,
            inputs=[
                gr.File(label="Upload PDF", file_types=[".pdf"]),
                gr.Textbox(label="Ask a question about the PDF")
            ],
            outputs=gr.Textbox(label="Answer"),
            title="PDF Question Answering System",
            description="Upload a PDF and ask questions about its content"
        )
        
        interface.launch()

    def run_cli(self):
        print("PDF Question Answering System")
        print("=" * 40)
        
        while True:
            print("\nOptions:")
            print("1. Upload and query PDF")
            print("2. Exit")
            
            choice = input("Select option (1-2): ").strip()
            
            if choice == "1":
                pdf_path = input("Enter PDF file path: ").strip()
                
                if not os.path.exists(pdf_path):
                    print("File not found!")
                    continue
                
                pdf_id = os.path.basename(pdf_path).replace('.pdf', '')
                
                print("Extracting text from PDF...")
                pages = self.extract_text_from_pdf(pdf_path)
                
                print("Chunking text...")
                chunks = self.chunk_text(pages)
                
                print("Storing embeddings...")
                self.store_embeddings(pdf_id, chunks)
                
                while True:
                    query = input("\nAsk a question (or 'done' to finish): ").strip()
                    
                    if query.lower() == 'done':
                        break
                    
                    print("Searching for relevant context...")
                    context_results = self.query_embeddings(pdf_id, query)
                    context_chunks = [result['text'] for result in context_results]
                    
                    print("Generating answer...")
                    answer = self.generate_answer(query, context_chunks)
                    print(f"\nAnswer: {answer}")
                
                self.delete_vectors_by_pdf_id(pdf_id)
                self.conversation_history = []
                
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid option!")