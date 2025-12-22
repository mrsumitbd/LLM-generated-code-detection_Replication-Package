from __future__ import annotations

import torch
from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class CheckpointConfig:
    """
    fsdp2 checkpoint config

    Attributes:
        enable_checkpoint (bool): Whether to enable checkpointing
        folder (str): The folder to store the checkpoints
        interval_type (str): Checkpointing interval unit of measurement ['step', 'seconds']
        interval (int): Checkpointing interval, in steps or seconds depending on --checkpoint.interval_type
        model_weights_only (bool): When model_weights_only=True, only model weights will be saved at the end of training.
                With this, checkpoints can be loaded using `torch.load(..., weights_only=True)` after conversion.
                When model_weights_only=False, the full checkpoint will be saved.
                A full checkpoint includes model, optimizer and train_state, which can be used to resume training.
                The default value is false.
        export_dtype (str): Converts to the specified precision when training completes and model_weights_only=true.
                Currently supports float32, float16, and bfloat16.
                The default value is float32.
        async_mode (str): Which async checkpoint mode to use. Currently there are 3 different modes.
                1. "disabled": synchronized checkpointing will be used.
                2. "async": torch.distributed.checkpoint.async_save will be used.
                3. "async_with_pinned_mem": this option utilizes a dedicated pinned memory
                   space and creates a separate process for faster GPU->CPU transfer
                   performance and eliminating GIL contention. The cost is increased CPU
                   memory usage. If insufficient CPU memory is available, performance may
                   degrade due to memory paging. For most users, "async" should suffice as
                   the performance overhead is typically small (on the order of tens of
                   seconds) compared to checkpointing frequency. This mode can be employed
                   to pursue near-zero checkpointing times (e.g., < 1 second) given
                   appropriate hardware support such as ample CPU memory and fast PCIe.

                "disabled" is the default mode.
        create_seed_checkpoint (bool): Initializes the full model without applying parallelisms, and then saves it as a seed checkpoint.
                Note: requires user to call train.py without specifying any parallelisms, e.g. NGPU=1.
                Could be implemented as a separate script, but this way shares more code.
    """

    enable_checkpoint: bool = False
    folder: str = "./checkpoints"
    interval_type: Literal["step", "seconds"] = "step"
    interval: int = 1
    model_weights_only: bool = False
    export_dtype: Literal["float32", "float16", "bfloat16"] = "float32"
    async_mode: Literal["disabled", "async", "async_with_pinned_mem"] = "disabled"
    create_seed_checkpoint: bool = False

    _VALID_INTERVAL_TYPES = {"step", "seconds"}
    _VALID_EXPORT_DTYPES = {"float32", "float16", "bfloat16"}
    _VALID_ASYNC_MODES = {"disabled", "async", "async_with_pinned_mem"}

    def __post_init__(self) -> None:
        if not isinstance(self.enable_checkpoint, bool):
            raise TypeError("enable_checkpoint must be a bool")
        if not isinstance(self.folder, str):
            raise TypeError("folder must be a str")
        if self.interval_type not in self._VALID_INTERVAL_TYPES:
            raise ValueError(
                f"interval_type must be one of {sorted(self._VALID_INTERVAL_TYPES)}"
            )
        if not isinstance(self.interval, int) or self.interval <= 0:
            raise ValueError("interval must be a positive integer")
        if not isinstance(self.model_weights_only, bool):
            raise TypeError("model_weights_only must be a bool")
        if self.export_dtype not in self._VALID_EXPORT_DTYPES:
            raise ValueError(
                f"export_dtype must be one of {sorted(self._VALID_EXPORT_DTYPES)}"
            )
        if self.async_mode not in self._VALID_ASYNC_MODES:
            raise ValueError(
                f"async_mode must be one of {sorted(self._VALID_ASYNC_MODES)}"
            )
        if not isinstance(self.create_seed_checkpoint, bool):
            raise TypeError("create_seed_checkpoint must be a bool")

    @property
    def export_torch_dtype(self) -> torch.dtype:
        """Return the corresponding torch dtype for export_dtype."""
        mapping = {
            "float32": torch.float32,
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        return mapping[self.export_dtype]

    def should_checkpoint(self, step: int, elapsed_seconds: float) -> bool:
        """Return True if a checkpoint should be performed at the given step or elapsed time."""
        if not self.enable_checkpoint:
            return False
        if self.interval_type == "step":
            return step % self.interval == 0
        return elapsed_seconds >= self.interval

    def __repr__(self) -> str:
        attrs = (
            f"enable_checkpoint={self.enable_checkpoint!r}",
            f"folder={self.folder!r}",
            f"interval_type={self.interval_type!r}",
            f"interval={self.interval!r}",
            f"model_weights_only={self.model_weights_only!r}",
            f"export_dtype={self.export_dtype!r}",
            f"async_mode={self.async_mode!r}",
            f"create_seed_checkpoint={self.create_seed_checkpoint!r}",
        )
        return f"{self.__class__.__name__}({', '.join(attrs)})"