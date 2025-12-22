import numpy as np
import torch
from .utils.dwpose.skeleton_extraction import draw_pose
from .utils.image_utils import tensor_to_pil, tensor_to_np, np_to_tensor, load_images_from_folder, Resize

class StableAnimatorSkeletonNode:
    """
    StableAnimator生成视频POSE骨架
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """定义输入参数"""
        return {
            "required": {
                "dwpose_detector_aligned":("DWPOSEDETECTORALIGNED",),
                "reference_image":("IMAGE",),
                "video_frames":("IMAGE",),
            },
        }

    FUNCTION = "extraction"
    CATEGORY = GLOBAL_CATEGORY

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("pose_frames",)

    def extraction(self, **kwargs):
        '''
        以下代码参考 StableAnimator.DWPose.dwpose_utils.dwpose_detector.get_video_pose, 以适应ComfyUI的参数输入
        '''
        dwpose_detector_aligned = kwargs["dwpose_detector_aligned"]
        ref_image = tensor_to_np(kwargs["reference_image"])
        height, width, _ = ref_image.shape
        ref_pose = dwpose_detector_aligned(ref_image)
        ref_keypoint_id = [0, 1, 2, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        ref_keypoint_id = [i for i in ref_keypoint_id \
            if len(ref_pose['bodies']['subset']) > 0 and ref_pose['bodies']['subset'][0][i] >= .0]
        ref_body = ref_pose['bodies']['candidate'][ref_keypoint_id]

        video_frames = kwargs["video_frames"]

        detected_poses = []
        for video_frame in video_frames:
            frame = tensor_to_np(video_frame.unsqueeze(0))
            frame = Resize.crop_center(frame, width, height)
            pose = dwpose_detector_aligned(frame)
            detected_poses.append(pose)
        
        detected_bodies = np.stack([p['bodies']['candidate'] for p in detected_poses if p['bodies']['candidate'].shape[0] == 18])[:,ref_keypoint_id]
        ay, by = np.polyfit(detected_bodies[:, :, 1].flatten(), np.tile(ref_body[:, 1], len(detected_bodies)), 1)
        fh = height
        fw = width
        ax = ay / (fh / fw / height * width)
        bx = np.mean(np.tile(ref_body[:, 0], len(detected_bodies)) - detected_bodies[:, :, 0].flatten() * ax)
        a = np.array([ax, ay])
        b = np.array([bx, by])
        
        output_pose = []
        for detected_pose in detected_poses:
            detected_pose['bodies']['candidate'] = detected_pose['bodies']['candidate'] * a + b
            detected_pose['faces'] = detected_pose['faces'] * a + b
            detected_pose['hands'] = detected_pose['hands'] * a + b
            im = draw_pose(detected_pose, height, width)
            output_pose.append(np_to_tensor(np.array(im)))
        
        output = torch.cat(output_pose, dim=0)
        return output,