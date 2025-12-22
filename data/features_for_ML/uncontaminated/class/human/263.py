import torch.utils.data
import torch
from typing import Any, TypeVar
import attrs
from imaginaire.model import ImaginaireModel
from megatron.core import ModelParallelConfig
from imaginaire.lazy_config import LazyDict
from imaginaire.utils import callback, distributed

class Config:
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    # Model configs.
    model: LazyDict[ImaginaireModel]
    # Optimizer configs.
    optimizer: LazyDict[torch.optim.Optimizer]
    # Scheduler configs.
    scheduler: LazyDict[torch.optim.lr_scheduler.LRScheduler]
    # Training data configs.
    dataloader_train: LazyDict[torch.utils.data.DataLoader]
    # Validation data configs.
    dataloader_val: LazyDict[torch.utils.data.DataLoader]

    # Training job configs.
    job: JobConfig = attrs.field(factory=JobConfig)

    # Trainer configs.
    trainer: TrainerConfig = attrs.field(factory=TrainerConfig)

    if USE_MEGATRON:
        # Megatron-Core configs
        model_parallel: ModelParallelConfig = attrs.field(factory=ModelParallelConfig)
    else:
        model_parallel: None = None

    # Checkpointer configs.
    checkpoint: CheckpointConfig = attrs.field(factory=CheckpointConfig)

    def pretty_print(self, use_color: bool = False) -> str:
        return _pretty_print_attrs_instance(self, 0, use_color)

    def to_dict(self) -> dict[str, Any]:
        return attrs.asdict(self)

    def validate(self) -> None:
        """Validate that the config has all required fields."""

        # broadcast job.name across all ranks to make sure it is consistent
        # otherwise, unaligned job names leads unaligned path to save checkpoints
        job_name_tensor = torch.ByteTensor(bytearray(self.job.name, "utf-8")).cuda()
        distributed.broadcast(job_name_tensor, 0)
        self.job.name = job_name_tensor.cpu().numpy().tobytes().decode("utf-8")

        assert self.job.project != ""
        assert self.job.group != ""
        assert self.job.name != ""