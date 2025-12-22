class StableAnimatorSkeletonNode:
    """
    StableAnimator生成视频POSE骨架
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return ["image", "video"]

    def extraction(self, **kwargs):
        if 'image' in kwargs:
            image_data = kwargs['image']
            # Perform extraction from image_data
            return "Skeleton extracted from image"
        elif 'video' in kwargs:
            video_data = kwargs['video']
            # Perform extraction from video_data
            return "Skeleton extracted from video"
        else:
            return "Invalid input type provided"