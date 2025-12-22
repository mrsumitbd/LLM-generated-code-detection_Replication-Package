import numpy as np

class StableAnimatorSkeletonNode:
    """
    StableAnimator生成视频POSE骨架
    """

    def __init__(self):
        self.skeleton_points = np.zeros((17, 2))
        self.skeleton_confidence = np.zeros(17)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "image": np.ndarray,
            "pose_2d": np.ndarray,
            "pose_confidence": np.ndarray
        }

    def extraction(self, **kwargs):
        image = kwargs["image"]
        pose_2d = kwargs["pose_2d"]
        pose_confidence = kwargs["pose_confidence"]

        self.skeleton_points = pose_2d
        self.skeleton_confidence = pose_confidence

        return self.skeleton_points, self.skeleton_confidence