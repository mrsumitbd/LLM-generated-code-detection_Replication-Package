import os
import math
from pathlib import Path
from typing import Iterable, List, Optional, Dict, Any

try:
    from PIL import Image
except ImportError:
    Image = None  # PIL is optional; if missing, run will raise an informative error


class FastModeRunner:
    """
    A lightweight runner that processes pairs of guide and style frames.
    The implementation is intentionally simple: it blends each guide frame
    with its corresponding style frame using a 50/50 alpha blend and writes
    the result to the specified output directory.

    Parameters
    ----------
    None

    Methods
    -------
    run(frames_guide, frames_style, batch_size, window_size,
        ebsynth_config, save_path=None)
        Process the frames and return a list of output file paths.
    """

    def __init__(self) -> None:
        # No initialization needed for this simple implementation
        pass

    def _ensure_pil(self) -> None:
        if Image is None:
            raise RuntimeError(
                "Pillow (PIL) is required for image processing but is not installed."
            )

    def _blend_frames(
        self, guide_path: Path, style_path: Path
    ) -> Image.Image:
        """
        Load two images and blend them with equal weight.

        Parameters
        ----------
        guide_path : Path
            Path to the guide image.
        style_path : Path
            Path to the style image.

        Returns
        -------
        Image.Image
            The blended image.
        """
        guide_img = Image.open(guide_path).convert("RGBA")
        style_img = Image.open(style_path).convert("RGBA")
        # Resize style to match guide if necessary
        if guide_img.size != style_img.size:
            style_img = style_img.resize(guide_img.size, Image.LANCZOS)
        blended = Image.blend(guide_img, style_img, alpha=0.5)
        return blended

    def run(
        self,
        frames_guide: Iterable[str],
        frames_style: Iterable[str],
        batch_size: int,
        window_size: int,
        ebsynth_config: Dict[str, Any],
        save_path: Optional[str] = None,
    ) -> List[str]:
        """
        Process the provided frames in batches and return the list of output
        file paths.

        Parameters
        ----------
        frames_guide : Iterable[str]
            Iterable of file paths to guide frames.
        frames_style : Iterable[str]
            Iterable of file paths to style frames.
        batch_size : int
            Number of frames to process in a single batch (unused in this
            implementation but kept for API compatibility).
        window_size : int
            Size of the processing window (unused in this implementation).
        ebsynth_config : dict
            Configuration dictionary for ebsynth (unused in this
            implementation).
        save_path : str, optional
            Directory where the processed frames will be written. If None,
            a temporary directory will be created.

        Returns
        -------
        List[str]
            List of file paths to the processed frames.
        """
        self._ensure_pil()

        guide_paths = [Path(p) for p in frames_guide]
        style_paths = [Path(p) for p in frames_style]

        if len(guide_paths) != len(style_paths):
            raise ValueError(
                "frames_guide and frames_style must contain the same number of items."
            )

        # Determine output directory
        out_dir = Path(save_path) if save_path else Path("fast_mode_output")
        out_dir.mkdir(parents=True, exist_ok=True)

        output_files: List[str] = []

        # Process in batches (batch_size and window_size are not used in this simple implementation)
        total_frames = len(guide_paths)
        num_batches = math.ceil(total_frames / batch_size)

        for batch_idx in range(num_batches):
            start = batch_idx * batch_size
            end = min(start + batch_size, total_frames)
            batch_guide = guide_paths[start:end]
            batch_style = style_paths[start:end]

            for g_path, s_path in zip(batch_guide, batch_style):
                blended_img = self._blend_frames(g_path, s_path)
                out_name = f"{g_path.stem}_blended{g_path.suffix}"
                out_path = out_dir / out_name
                blended_img.save(out_path)
                output_files.append(str(out_path))

        return output_files