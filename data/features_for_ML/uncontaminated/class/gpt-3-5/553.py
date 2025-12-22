class ImageDublicator:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            'image': str,
            'count': int
        }

    def execute(self, image, count):
        duplicated_images = [image] * count
        return duplicated_images