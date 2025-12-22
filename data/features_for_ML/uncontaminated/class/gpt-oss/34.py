import os
import json
import argparse
import tempfile
import boto3
import faiss
import numpy as np
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import gradio as gr

class ImageSearch:
    def __init__(self, s3_bucket, index_file="faiss.index",
                 metadata_file="metadata.json", embedding_length=512,
                 region_name=None):
        """
        Initialize the ImageSearch object.

        Parameters
        ----------
        s3_bucket : str
            Name of the S3 bucket containing images.
        index_file : str, optional
            Key name for the FAISS index file in S3.
        metadata_file : str, optional
            Key name for the metadata JSON file in S3.
        embedding_length : int, optional
            Dimensionality of the embeddings (default 512 for CLIP).
        region_name : str, optional
            AWS region name for the S3 client.
        """
        self.s3_bucket = s3_bucket
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.embedding_length = embedding_length
        self.region_name = region_name

        self.s3 = boto3.client('s3', region_name=self.region_name)

        # Load CLIP model and processor
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

        self.index = None
        self.metadata = None

    # ------------------------------------------------------------------
    # Index building and loading
    # ------------------------------------------------------------------
    def build_index(self, prefix=""):
        """
        Build a FAISS index from images stored in the S3 bucket.

        Parameters
        ----------
        prefix : str, optional
            Prefix to filter objects in the bucket.
        """
        # List all objects under the prefix
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.s3_bucket, Prefix=prefix)

        image_keys = []
        for page in page_iterator:
            for obj in page.get('Contents', []):
                key = obj['Key']
                if key.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                    image_keys.append(key)

        if not image_keys:
            print("No images found.")
            return

        embeddings = []
        metadata = []

        for key in tqdm(image_keys, desc="Processing images"):
            obj = self.s3.get_object(Bucket=self.s3_bucket, Key=key)
            img_bytes = obj['Body'].read()
            image = Image.open(BytesIO(img_bytes)).convert("RGB")

            # Compute image embedding
            inputs = self.processor(images=image, return_tensors="pt", padding=True)
            with torch.no_grad():
                image_emb = self.model.get_image_features(**inputs)
            image_emb = image_emb / image_emb.norm(p=2, dim=-1, keepdim=True)
            embeddings.append(image_emb.cpu().numpy())

            # Store metadata
            folder = os.path.dirname(key)
            filename = os.path.basename(key)
            metadata.append({
                "id": len(metadata),
                "s3_key": key,
                "folder": folder,
                "filename": filename
            })

        embeddings = np.vstack(embeddings).astype('float32')

        # Build FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_length)
        self.index.add(embeddings)

        self.metadata = metadata

        # Save index to bytes
        index_bytes = faiss.serialize_index(self.index)

        # Upload index and metadata to S3
        self.s3.put_object(Bucket=self.s3_bucket, Key=self.index_file, Body=index_bytes)
        self.s3.put_object(Bucket=self.s3_bucket, Key=self.metadata_file,
                           Body=json.dumps(self.metadata).encode('utf-8'))

        print(f"Index built and uploaded to s3://{self.s3_bucket}/{self.index_file}")

    def load_index(self):
        """
        Load the FAISS index and metadata from S3 into memory.
        """
        # Download index
        index_obj = self.s3.get_object(Bucket=self.s3_bucket, Key=self.index_file)
        index_bytes = index_obj['Body'].read()
        self.index = faiss.deserialize_index(index_bytes)

        # Download metadata
        meta_obj = self.s3.get_object(Bucket=self.s3_bucket, Key=self.metadata_file)
        meta_bytes = meta_obj['Body'].read()
        self.metadata = json.loads(meta_bytes.decode('utf-8'))

        print(f"Index and metadata loaded from s3://{self.s3_bucket}")

    # ------------------------------------------------------------------
    # Search functions
    # ------------------------------------------------------------------
    def _embed_text(self, text):
        """
        Compute CLIP text embedding for a given query string.
        """
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            text_emb = self.model.get_text_features(**inputs)
        text_emb = text_emb / text_emb.norm(p=2, dim=-1, keepdim=True)
        return text_emb.cpu().numpy()

    def _embed_image(self, image):
        """
        Compute CLIP image embedding for a PIL.Image or file path.
        """
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            img_emb = self.model.get_image_features(**inputs)
        img_emb = img_emb / img_emb.norm(p=2, dim=-1, keepdim=True)
        return img_emb.cpu().numpy()

    def search(self, text_query, k=5, folder=None):
        """
        Search the index using a text query.

        Parameters
        ----------
        text_query : str
            The query string.
        k : int, optional
            Number of nearest neighbors to return.
        folder : str, optional
            Restrict search to a specific folder prefix.

        Returns
        -------
        list of dict
            Each dict contains metadata and distance.
        """
        if self.index is None or self.metadata is None:
            self.load_index()

        query_emb = self._embed_text(text_query)

        # If folder filter is requested, create mask
        if folder:
            indices = [m["id"] for m in self.metadata if m["folder"].startswith(folder)]
            if not indices:
                return []
            mask = np.zeros(len(self.metadata), dtype=bool)
            mask[indices] = True
            # Filter index
            sub_index = faiss.IndexFlatL2(self.embedding_length)
            sub_index.add(self.index.reconstruct_n(0, len(self.metadata)))
            sub_index = faiss.IndexIVFFlat(sub_index, self.embedding_length, 1, faiss.METRIC_L2)
            sub_index.train(sub_index.reconstruct_n(0, len(self.metadata)))
            sub_index.add(sub_index.reconstruct_n(0, len(self.metadata)))
            sub_index = faiss.IndexPreTransform(sub_index, mask.astype(np.float32))
            D, I = sub_index.search(query_emb, k)
        else:
            D, I = self.index.search(query_emb, k)

        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx]
            results.append({
                "metadata": meta,
                "distance": float(dist)
            })
        return results

    def search_by_image(self, image, k=5, folder=None):
        """
        Search the index using an image.

        Parameters
        ----------
        image : PIL.Image or str
            Image to query.
        k : int, optional
            Number of nearest neighbors to return.
        folder : str, optional
            Restrict search to a specific folder prefix.

        Returns
        -------
        list of dict
            Each dict contains metadata and distance.
        """
        if self.index is None or self.metadata is None:
            self.load_index()

        query_emb = self._embed_image(image)

        if folder:
            indices = [m["id"] for m in self.metadata if m["folder"].startswith(folder)]
            if not indices:
                return []
            mask = np.zeros(len(self.metadata), dtype=bool)
            mask[indices] = True
            sub_index = faiss.IndexFlatL2(self.embedding_length)
            sub_index.add(self.index.reconstruct_n(0, len(self.metadata)))
            sub_index = faiss.IndexIVFFlat(sub_index, self.embedding_length, 1, faiss.METRIC_L2)
            sub_index.train(sub_index.reconstruct_n(0, len(self.metadata)))
            sub_index.add(sub_index.reconstruct_n(0, len(self.metadata)))
            sub_index = faiss.IndexPreTransform(sub_index, mask.astype(np.float32))
            D, I = sub_index.search(query_emb, k)
        else:
            D, I = self.index.search(query_emb, k)

        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx]
            results.append({
                "metadata": meta,
                "distance": float(dist)
            })
        return results

    # ------------------------------------------------------------------
    # Utility functions
    # ------------------------------------------------------------------
    def get_folders(self):
        """
        List all folder prefixes in the S3 bucket.
        """
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.s3_bucket, Delimiter='/')

        prefixes = []
        for page in page_iterator:
            for prefix in page.get('CommonPrefixes', []):
                prefixes.append(prefix['Prefix'])
        return prefixes

    # ------------------------------------------------------------------
    # Gradio interface
    # ------------------------------------------------------------------
    def _gradio_search(self, query, k, folder):
        results = self.search(query, k=int(k), folder=folder)
        outputs = []
        for r in results:
            meta = r["metadata"]
            key = meta["s3_key"]
            obj = self.s3.get_object(Bucket=self.s3_bucket, Key=key)
            img_bytes = obj['Body'].read()
            outputs.append((Image.open(BytesIO(img_bytes)), meta["filename"], f"Dist: {r['distance']:.4f}"))
        return outputs

    def _gradio_search_image(self, image, k, folder):
        if image is None:
            return []
        results = self.search_by_image(image, k=int(k), folder=folder)
        outputs = []
        for r in results:
            meta = r["metadata"]
            key = meta["s3_key"]
            obj = self.s3.get_object(Bucket=self.s3_bucket, Key=key)
            img_bytes = obj['Body'].read()
            outputs.append((Image.open(BytesIO(img_bytes)), meta["filename"], f"Dist: {r['distance']:.4f}"))
        return outputs

    def start_gradio(self):
        """
        Launch a Gradio web interface for text and image search.
        """
        folders = self.get_folders()
        with gr.Blocks() as demo:
            gr.Markdown("# Image Search Demo")
            with gr.Tab("Text Search"):
                with gr.Row():
                    txt_query = gr.Textbox(label="Text Query")
                    txt_k = gr.Slider(1, 20, value=5, step=1, label="k")
                    txt_folder = gr.Dropdown(choices=folders, label="Folder (optional)", allow_custom_value=True)
                txt_btn = gr.Button("Search")
                txt_output = gr.Gallery(label="Results", show_label=True, elem_id="gallery")
                txt_btn.click(fn=self._gradio_search, inputs=[txt_query, txt_k, txt_folder], outputs=txt_output)

            with gr.Tab("Image Search"):
                with gr.Row():
                    img_input = gr.Image(type="pil", label="Upload Image")
                    img_k = gr.Slider(1, 20, value=5, step=1, label="k")
                    img_folder = gr.Dropdown(choices=folders, label="Folder (optional)", allow_custom_value=True)
                img_btn = gr.Button("Search")
                img_output = gr.Gallery(label="Results", show_label=True, elem_id="gallery")
                img_btn.click(fn=self._gradio_search_image, inputs=[img_input, img_k, img_folder], outputs=img_output)

        demo.launch()

    # ------------------------------------------------------------------
    # CLI
    # ------------------------------------------------------------------
    def run_cli(self):
        parser = argparse.ArgumentParser(description="ImageSearch CLI")
        sub = parser.add_subparsers(dest="command")

        build = sub.add_parser("build", help="Build index")
        build.add_argument("--prefix", default="", help="S3 prefix to filter images")

        load = sub.add_parser("load", help="Load index into memory")

        search = sub.add_parser("search", help="Search by text")
        search.add_argument("query", help="Text query")
        search.add_argument("--k", type=int, default=5, help="Number of results")
        search.add_argument("--folder", default=None, help="Folder prefix")

        search_img = sub.add_parser("search_image", help="Search by image")
        search_img.add_argument("image_path", help="Path to image file")
        search_img.add_argument("--k", type=int, default=5, help="Number of results")
        search_img.add_argument("--folder", default=None, help="Folder prefix")

        folders = sub.add_parser("folders", help="List folders")

        gradio = sub.add_parser("gradio", help="Start Gradio UI")

        args = parser.parse_args()

        if args.command == "build":
            self.build_index(prefix=args.prefix)
        elif args.command == "load":
            self.load_index()
        elif args.command == "search":
            self.load_index()
            results = self.search(args.query, k=args.k, folder=args.folder)
            for r in results:
                meta = r["metadata"]
                print(f"{meta['filename']} (dist={r['distance']:.4f}) - s3://{self.s3_bucket}/{meta['s3_key']}")
        elif args.command == "search_image":
            self.load_index()
            img = Image.open(args.image_path).convert("RGB")
            results = self.search_by_image(img, k=args.k, folder=args.folder)
            for r in results:
                meta = r["metadata"]
                print(f"{meta['filename']} (dist={r['distance']:.4f}) - s3://{self.s3_bucket}/{meta['s3_key']}")
        elif args.command == "folders":
            self.load_index()
            for p in self.get_folders():
                print(p)
        elif args.command == "gradio":
            self.start_gradio()
        else:
            parser.print_help()