import os
from typing import Optional


class RotateMatrixConfig:
    """Configuration for Rotate Matrix dataset generation"""

    def __init__(
        self,
        matrix_size: int,
        rotation_angle: float,
        seed: Optional[int] = None,
        output_dir: Optional[str] = None,
    ):
        self.matrix_size = matrix_size
        self.rotation_angle = rotation_angle
        self.seed = seed
        self.output_dir = output_dir

    def validate(self):
        # Validate matrix_size
        if not isinstance(self.matrix_size, int):
            raise TypeError(
                f"matrix_size must be an int, got {type(self.matrix_size).__name__}"
            )
        if self.matrix_size <= 0:
            raise ValueError("matrix_size must be a positive integer")

        # Validate rotation_angle
        if not isinstance(self.rotation_angle, (int, float)):
            raise TypeError(
                f"rotation_angle must be a number, got {type(self.rotation_angle).__name__}"
            )
        if not (0 <= self.rotation_angle <= 360):
            raise ValueError("rotation_angle must be between 0 and 360 degrees")

        # Validate seed
        if self.seed is not None and not isinstance(self.seed, int):
            raise TypeError(f"seed must be an int, got {type(self.seed).__name__}")

        # Validate output_dir
        if self.output_dir is not None:
            if not isinstance(self.output_dir, str):
                raise TypeError(
                    f"output_dir must be a string, got {type(self.output_dir).__name__}"
                )
            # Ensure the directory exists or can be created
            try:
                os.makedirs(self.output_dir, exist_ok=True)
            except Exception as exc:
                raise ValueError(
                    f"Could not create or access output_dir '{self.output_dir}': {exc}"
                )