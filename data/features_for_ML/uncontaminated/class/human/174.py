from ..patch_match import PyramidPatchMatcher
from PIL import Image
import functools, os

class FastModeRunner:
    def __init__(self):
        pass

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config, save_path=None):
        frames_guide = frames_guide.raw_data()
        frames_style = frames_style.raw_data()
        table_manager = TableManager()
        patch_match_engine = PyramidPatchMatcher(
            image_height=frames_style[0].shape[0],
            image_width=frames_style[0].shape[1],
            channel=3,
            **ebsynth_config
        )
        # left part
        table_l = table_manager.build_remapping_table(frames_guide, frames_style, patch_match_engine, batch_size, desc="Fast Mode Step 1/4")
        table_l = table_manager.remapping_table_to_blending_table(table_l)
        table_l = table_manager.process_window_sum(frames_guide, table_l, patch_match_engine, window_size, batch_size, desc="Fast Mode Step 2/4")
        # right part
        table_r = table_manager.build_remapping_table(frames_guide[::-1], frames_style[::-1], patch_match_engine, batch_size, desc="Fast Mode Step 3/4")
        table_r = table_manager.remapping_table_to_blending_table(table_r)
        table_r = table_manager.process_window_sum(frames_guide[::-1], table_r, patch_match_engine, window_size, batch_size, desc="Fast Mode Step 4/4")[::-1]
        # merge
        frames = []
        for (frame_l, weight_l), frame_m, (frame_r, weight_r) in zip(table_l, frames_style, table_r):
            weight_m = -1
            weight = weight_l + weight_m + weight_r
            frame = frame_l * (weight_l / weight) + frame_m * (weight_m / weight) + frame_r * (weight_r / weight)
            frames.append(frame)
        frames = [frame.clip(0, 255).astype("uint8") for frame in frames]
        if save_path is not None:
            for target, frame in enumerate(frames):
                Image.fromarray(frame).save(os.path.join(save_path, "%05d.png" % target))