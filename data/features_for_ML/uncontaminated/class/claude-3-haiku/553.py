class ImageDublicator:

    @classmethod
    def INPUT_TYPES(cls):
        return ['image', 'count']

    def execute(self, image, count):
        duplicated_images = []
        for _ in range(count):
            duplicated_images.append(image.copy())
        return duplicated_images