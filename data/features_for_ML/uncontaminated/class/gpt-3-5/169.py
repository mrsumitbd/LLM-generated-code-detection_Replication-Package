class BaseImageUploader:
    
    def upload_file(self, filename):
        # Implement the file uploading logic here
        print(f"Uploading file: {filename}")  # Example implementation, replace with actual logic

# Example usage
uploader = BaseImageUploader()
uploader.upload_file("image.jpg")