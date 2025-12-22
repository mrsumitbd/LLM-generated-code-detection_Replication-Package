import datetime
from typing import Any, Dict, Optional

class CheckpointState:
    """State of model, optimizer, and scheduler after a given number of epochs."""

    def __init__(
        self,
        epoch: int = 0,
        model_state_dict: Optional[Dict[str, Any]] = None,
        optimizer_state_dict: Optional[Dict[str, Any]] = None,
        scheduler_state_dict: Optional[Dict[str, Any]] = None,
        loss: Optional[float] = None,
        metrics: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> None:
        self.epoch = epoch
        self.model_state_dict = model_state_dict or {}
        self.optimizer_state_dict = optimizer_state_dict or {}
        self.scheduler_state_dict = scheduler_state_dict or {}
        self.loss = loss
        self.metrics = metrics or {}
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary representation of the checkpoint."""
        return {
            "epoch": self.epoch,
            "model_state_dict": self.model_state_dict,
            "optimizer_state_dict": self.optimizer_state_dict,
            "scheduler_state_dict": self.scheduler_state_dict,
            "loss": self.loss,
            "metrics": self.metrics,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CheckpointState":
        """Create a CheckpointState instance from a dictionary."""
        return cls(
            epoch=data.get("epoch", 0),
            model_state_dict=data.get("model_state_dict", {}),
            optimizer_state_dict=data.get("optimizer_state_dict", {}),
            scheduler_state_dict=data.get("scheduler_state_dict", {}),
            loss=data.get("loss"),
            metrics=data.get("metrics", {}),
            timestamp=data.get("timestamp"),
        )

    def save(self, path: str) -> None:
        """Save the checkpoint to a file using torch.save."""
        import torch

        torch.save(self.to_dict(), path)

    @classmethod
    def load(cls, path: str) -> "CheckpointState":
        """Load a checkpoint from a file using torch.load."""
        import torch

        data = torch.load(path, map_location="cpu")
        return cls.from_dict(data)

    def __repr__(self) -> str:
        return (
            f"<CheckpointState epoch={self.epoch} loss={self.loss} "
            f"metrics={self.metrics} timestamp={self.timestamp}>"
        )

    # Convenience setters
    def set_model_state(self, state: Dict[str, Any]) -> None:
        self.model_state_dict = state

    def set_optimizer_state(self, state: Dict[str, Any]) -> None:
        self.optimizer_state_dict = state

    def set_scheduler_state(self, state: Dict[str, Any]) -> None:
        self.scheduler_state_dict = state

    def set_loss(self, loss: float) -> None:
        self.loss = loss

    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        self.metrics = metrics

    def set_epoch(self, epoch: int) -> None:
        self.epoch = epoch