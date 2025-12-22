import gradio as gr

class ImageSearch:

    def __init__(self, s3_bucket, index_file="faiss.index", metadata_file="metadata.json", embedding_length=1024, region_name=None):
        self.s3_bucket = s3_bucket
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.embedding_length = embedding_length
        self.region_name = region_name

    def build_index(self, prefix=""):
        # Implement build_index logic here
        pass

    def load_index(self):
        # Implement load_index logic here
        pass

    def search(self, text_query, k=5, folder=None):
        # Implement search logic here
        pass

    def search_by_image(self, image, k=5, folder=None):
        # Implement search_by_image logic here
        pass

    def get_folders(self):
        # Implement get_folders logic here
        pass

    def start_gradio(self):
        # Implement start_gradio logic here
        pass

    def run_cli(self):
        # Implement run_cli logic here
        pass