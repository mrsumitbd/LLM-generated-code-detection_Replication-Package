import os
import json
import numpy as np
import faiss
import boto3
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import gradio as gr
from PIL import Image
import io
import clip
import torch

class ImageSearch:

    def __init__(self, s3_bucket, index_file="faiss.index", metadata_file="metadata.json", embedding_length=1024, region_name=None):
        self.s3_bucket = s3_bucket
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.embedding_length = embedding_length
        self.region_name = region_name or "us-east-1"
        
        self.s3_client = boto3.client("s3", region_name=self.region_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        self.index = None
        self.metadata = []
        self.folders = set()
        
    def build_index(self, prefix=""):
        """Build FAISS index from images in S3 bucket"""
        self.metadata = []
        self.folders = set()
        embeddings = []
        
        paginator = self.s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.s3_bucket, Prefix=prefix)
        
        for page in pages:
            if "Contents" not in page:
                continue
                
            for obj in page["Contents"]:
                key = obj["Key"]
                
                if not any(key.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    continue
                
                folder = str(Path(key).parent)
                if folder != ".":
                    self.folders.add(folder)
                
                try:
                    response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=key)
                    image_data = response["Body"].read()
                    image = Image.open(io.BytesIO(image_data)).convert("RGB")
                    
                    with torch.no_grad():
                        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                        embedding = self.model.encode_image(image_input).cpu().numpy().flatten()
                    
                    embeddings.append(embedding)
                    self.metadata.append({
                        "key": key,
                        "folder": folder,
                        "size": obj["Size"]
                    })
                except Exception as e:
                    print(f"Error processing {key}: {e}")
                    continue
        
        if embeddings:
            embeddings = np.array(embeddings).astype("float32")
            faiss.normalize_L2(embeddings)
            
            self.index = faiss.IndexFlatIP(self.embedding_length)
            self.index.add(embeddings)
            
            self._save_index()
    
    def load_index(self):
        """Load FAISS index and metadata from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=self.index_file)
            index_data = response["Body"].read()
            
            with open("/tmp/faiss.index", "wb") as f:
                f.write(index_data)
            
            self.index = faiss.read_index("/tmp/faiss.index")
            
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=self.metadata_file)
            metadata_data = response["Body"].read()
            self.metadata = json.loads(metadata_data)
            
            self.folders = set(item["folder"] for item in self.metadata)
            
        except Exception as e:
            print(f"Error loading index: {e}")
    
    def _save_index(self):
        """Save FAISS index and metadata to S3"""
        try:
            faiss.write_index(self.index, "/tmp/faiss.index")
            
            with open("/tmp/faiss.index", "rb") as f:
                self.s3_client.upload_fileobj(f, self.s3_bucket, self.index_file)
            
            metadata_json = json.dumps(self.metadata)
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=self.metadata_file,
                Body=metadata_json
            )
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def search(self, text_query: str, k: int = 5, folder: Optional[str] = None) -> List[Dict]:
        """Search by text query"""
        if self.index is None:
            self.load_index()
        
        with torch.no_grad():
            text_input = clip.tokenize([text_query]).to(self.device)
            text_embedding = self.model.encode_text(text_input).cpu().numpy().flatten()
        
        text_embedding = text_embedding.astype("float32").reshape(1, -1)
        faiss.normalize_L2(text_embedding)
        
        distances, indices = self.index.search(text_embedding, k * 3)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                item = self.metadata[idx]
                if folder is None or item["folder"] == folder:
                    results.append({
                        "key": item["key"],
                        "folder": item["folder"],
                        "score": float(distance)
                    })
                    if len(results) >= k:
                        break
        
        return results[:k]
    
    def search_by_image(self, image: Image.Image, k: int = 5, folder: Optional[str] = None) -> List[Dict]:
        """Search by image"""
        if self.index is None:
            self.load_index()
        
        image = image.convert("RGB")
        
        with torch.no_grad():
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            image_embedding = self.model.encode_image(image_input).cpu().numpy().flatten()
        
        image_embedding = image_embedding.astype("float32").reshape(1, -1)
        faiss.normalize_L2(image_embedding)
        
        distances, indices = self.index.search(image_embedding, k * 3)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                item = self.metadata[idx]
                if folder is None or item["folder"] == folder:
                    results.append({
                        "key": item["key"],
                        "folder": item["folder"],
                        "score": float(distance)
                    })
                    if len(results) >= k:
                        break
        
        return results[:k]
    
    def get_folders(self) -> List[str]:
        """Get list of folders in index"""
        if not self.folders and self.metadata:
            self.folders = set(item["folder"] for item in self.metadata)
        return sorted(list(self.folders))
    
    def start_gradio(self):
        """Start Gradio interface"""
        if self.index is None:
            self.load_index()
        
        def search_interface(query_type, query_input, k, folder_filter):
            try:
                if query_type == "Text":
                    results = self.search(query_input, k=k, folder=folder_filter if folder_filter != "All" else None)
                else:
                    if isinstance(query_input, str):
                        image = Image.open(query_input)
                    else:
                        image = query_input
                    results = self.search_by_image(image, k=k, folder=folder_filter if folder_filter != "All" else None)
                
                output_html = "<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px;'>"
                for result in results:
                    try:
                        response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=result["key"])
                        image_data = response["Body"].read()
                        image_b64 = __import__('base64').b64encode(image_data).decode()
                        output_html += f"<div><img src='data:image/jpeg;base64,{image_b64}' style='width: 100%; border-radius: 5px;'><p>{result['key']}<br>Score: {result['score']:.3f}</p></div>"
                    except:
                        pass
                output_html += "</div>"
                
                return output_html
            except Exception as e:
                return f"Error: {str(e)}"
        
        folders = ["All"] + self.get_folders()
        
        with gr.Blocks() as demo:
            gr.Markdown("# Image Search")
            
            with gr.Row():
                query_type = gr.Radio(["Text", "Image"], value="Text", label="Query Type")
                k = gr.Slider(1, 20, value=5, step=1, label="Number of Results")
                folder_filter = gr.Dropdown(folders, value="All", label="Filter by Folder")
            
            with gr.Row():
                query_input = gr.Textbox(label="Text Query", visible=True)
                image_input = gr.Image(label="Image Query", visible=False, type="pil")
            
            def update_input_visibility(query_type_val):
                return gr.Textbox(visible=(query_type_val == "Text")), gr.Image(visible=(query_type_val == "Image"))
            
            query_type.change(update_input_visibility, inputs=query_type, outputs=[query_input, image_input])
            
            search_button = gr.Button("Search")
            output = gr.HTML()
            
            search_button.click(
                search_interface,
                inputs=[query_type, query_input, k, folder_filter],
                outputs=output
            )
        
        demo.launch()
    
    def run_cli(self):
        """Run CLI interface"""
        if self.index is None:
            self.load_index()
        
        while True:
            print("\n=== Image Search CLI ===")
            print("1. Search by text")
            print("2. Search by image file")
            print("3. Build index")
            print("4. Exit")
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                query = input("Enter text query: ").strip()
                k = int(input("Number of results (default 5): ") or "5")
                results = self.search(query, k=k)
                
                print("\nResults:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['key']} (Score: {result['score']:.3f})")
            
            elif choice == "2":
                image_path = input("Enter image file path: ").strip()
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    k = int(input("Number of results (default 5): ") or "5")
                    results = self.search_by_image(image, k=k)
                    
                    print("\nResults:")
                    for i, result in enumerate(results, 1):
                        print(f"{i}. {result['key']} (Score: {result['score']:.3f})")
                else:
                    print("File not found")
            
            elif choice == "3":
                prefix = input("Enter S3 prefix (default ''): ").strip()
                print("Building index...")
                self.build_index(prefix=prefix)
                print("Index built successfully")
            
            elif choice == "4":
                break
            
            else:
                print("Invalid option")