import anthropic
import json
from dataclasses import dataclass, asdict


@dataclass
class CheckpointState:
    """State of model, optimizer, and scheduler after a given number of epochs."""
    epoch: int
    model_state: dict
    optimizer_state: dict
    scheduler_state: dict
    metrics: dict
    
    def to_dict(self) -> dict:
        """Convert checkpoint state to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert checkpoint state to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict) -> "CheckpointState":
        """Create checkpoint state from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "CheckpointState":
        """Create checkpoint state from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, filepath: str) -> None:
        """Save checkpoint state to file."""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def load(cls, filepath: str) -> "CheckpointState":
        """Load checkpoint state from file."""
        with open(filepath, 'r') as f:
            return cls.from_json(f.read())
    
    def get_summary(self) -> str:
        """Get a summary of the checkpoint state using Claude."""
        client = anthropic.Anthropic()
        
        checkpoint_info = f"""
        Epoch: {self.epoch}
        Model State Keys: {list(self.model_state.keys())}
        Optimizer State Keys: {list(self.optimizer_state.keys())}
        Scheduler State Keys: {list(self.scheduler_state.keys())}
        Metrics: {self.metrics}
        """
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a brief summary of this training checkpoint state:\n{checkpoint_info}"
                }
            ]
        )
        
        return message.content[0].text


def main():
    """Test the CheckpointState class."""
    checkpoint = CheckpointState(
        epoch=10,
        model_state={"layer1": [1, 2, 3], "layer2": [4, 5, 6]},
        optimizer_state={"lr": 0.001, "momentum": 0.9},
        scheduler_state={"step": 10, "last_lr": 0.001},
        metrics={"loss": 0.25, "accuracy": 0.95}
    )
    
    print("Checkpoint State:")
    print(f"  Epoch: {checkpoint.epoch}")
    print(f"  Metrics: {checkpoint.metrics}")
    
    print("\nJSON representation:")
    print(checkpoint.to_json())
    
    print("\nGetting summary from Claude...")
    summary = checkpoint.get_summary()
    print(f"Summary:\n{summary}")


if __name__ == "__main__":
    main()