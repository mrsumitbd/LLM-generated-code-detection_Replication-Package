import os
from PIL import Image
import gradio as gr

class ImageSearch:
    def __init__(self, s3_bucket, index_file="faiss.index", metadata_file="metadata.json", embedding_length=1024, region_name=None):
        self.s3_bucket = s3_bucket
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.s3_utils = S3Utils()
        self.embedder = Embedder(embedding_length=embedding_length, region_name=region_name)
        self.vectorstore = VectorStore()
        self.index_loaded = False

    def build_index(self, prefix=""):
        print(f"Building index from images in S3 bucket: {self.s3_bucket}, prefix: '{prefix}'")
        image_info_list = self.s3_utils.get_image_keys_with_folders(self.s3_bucket, prefix)
        embeddings, processed_image_info = self.embedder.get_image_embeddings(image_info_list, self.s3_utils)
        self.vectorstore.build_and_save_index(embeddings, processed_image_info, self.index_file, self.metadata_file, self.s3_utils, self.s3_bucket)
        print("Index built and saved.")

    def load_index(self):
        self.vectorstore.load_index_and_metadata(self.index_file, self.metadata_file)
        self.index_loaded = True

    def search(self, text_query, k=5, folder=None):
        if not self.index_loaded:
            self.load_index()
        query_embedding = self.embedder.get_text_embedding(text_query)
        results = self.vectorstore.search_images(query_embedding, k=k, filter_folder=folder)
        return [
            {
                "distance": float(distance),
                "s3_path": s3_path,
                "folder": folder_name,
                "image_url": self.s3_utils.get_image_url_from_s3_path(s3_path)
            }
            for distance, s3_path, folder_name in results
        ]

    def search_by_image(self, image, k=5, folder=None):
        if not self.index_loaded:
            self.load_index()
        query_embedding = self.embedder.get_image_embedding_from_pil(image)
        results = self.vectorstore.search_images(query_embedding, k=k, filter_folder=folder)
        return [
            {
                "distance": float(distance),
                "s3_path": s3_path,
                "folder": folder_name,
                "image_url": self.s3_utils.get_image_url_from_s3_path(s3_path)
            }
            for distance, s3_path, folder_name in results
        ]

    def get_folders(self):
        if not self.index_loaded:
            self.load_index()
        return self.vectorstore.get_unique_folder_names()

    # --- Gradio UI ---
    def start_gradio(self):
        def text_search_interface(text_query, k, folder):
            results = self.search(text_query, k=k, folder=folder if folder != "All" else None)
            return [r["image_url"] for r in results]
        def image_search_interface(image, k, folder):
            if image is None:
                return []
            pil_image = image if isinstance(image, Image.Image) else Image.open(image)
            results = self.search_by_image(pil_image, k=k, folder=folder if folder != "All" else None)
            return [r["image_url"] for r in results]
        folder_choices = ["All"] + self.get_folders()
        text_tab = gr.Interface(
            fn=text_search_interface,
            inputs=[
                gr.Textbox(label="Text Query", placeholder="Describe the image you want..."),
                gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Top K Results"),
                gr.Dropdown(choices=folder_choices, value="All", label="Folder (optional)")
            ],
            outputs=gr.Gallery(label="Search Results"),
            title="Text to Image Search"
        )
        image_tab = gr.Interface(
            fn=image_search_interface,
            inputs=[
                gr.Image(type="pil", label="Query Image"),
                gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Top K Results"),
                gr.Dropdown(choices=folder_choices, value="All", label="Folder (optional)")
            ],
            outputs=gr.Gallery(label="Search Results"),
            title="Image to Image Search"
        )
        tabs = gr.TabbedInterface([text_tab, image_tab], tab_names=["Text to Image", "Image to Image"])
        return tabs.launch(share=True)

    # --- CLI ---
    def run_cli(self):
        print("Image Search CLI initialized.")
        print("Type 'exit' or 'quit' to end.")
        while True:
            mode = input("\nChoose search mode: (1) Text, (2) Image, (exit/quit): ").strip().lower()
            if mode in ["exit", "quit"]:
                print("Goodbye!")
                break
            if mode == "1" or mode.startswith("text"):
                text = input("Enter your search query: ")
                k = input("How many results? (default 5): ")
                k = int(k) if k.strip().isdigit() else 5
                folder = input("Filter by folder (leave blank for all): ")
                folder = folder.strip() or None
                try:
                    results = self.search(text, k=k, folder=folder)
                    print("\nResults:")
                    for r in results:
                        print(f"{r['image_url']} (distance: {r['distance']:.4f}, folder: {r['folder']})")
                except Exception as e:
                    print(f"Error: {str(e)}")
            elif mode == "2" or mode.startswith("image"):
                image_path = input("Enter path to query image: ").strip()
                if not os.path.exists(image_path):
                    print(f"File not found: {image_path}")
                    continue
                try:
                    pil_image = Image.open(image_path).convert("RGB")
                    k = input("How many results? (default 5): ")
                    k = int(k) if k.strip().isdigit() else 5
                    folder = input("Filter by folder (leave blank for all): ")
                    folder = folder.strip() or None
                    results = self.search_by_image(pil_image, k=k, folder=folder)
                    print("\nResults:")
                    for r in results:
                        print(f"{r['image_url']} (distance: {r['distance']:.4f}, folder: {r['folder']})")
                except Exception as e:
                    print(f"Error: {str(e)}")
            else:
                print("Invalid mode. Please enter 1 for Text, 2 for Image, or exit/quit.")