class BaseImageUploader:
    def __init__(self, storage_provider, bucket_name):
        self.storage_provider = storage_provider
        self.bucket_name = bucket_name

    def upload_file(self, filename):
        with open(filename, 'rb') as file:
            file_content = file.read()
        self.storage_provider.upload_object(self.bucket_name, filename, file_content)