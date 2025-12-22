from dataclasses import dataclass, field

# Simple registry of model configurations
_MODEL_REGISTRY = {
    "gpt2": {"layers": 12, "hidden_size": 768},
    "bert-base": {"layers": 12, "hidden_size": 768},
    "bert-large": {"layers": 24, "hidden_size": 1024},
}

@dataclass
class ModelArgs:
    name: str
    config: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.config, dict):
            raise TypeError("config must be a dict")
        # Ensure some default keys exist
        self.config.setdefault("layers", 12)
        self.config.setdefault("hidden_size", 768)

    @classmethod
    def from_name(cls, name: str):
        config = _MODEL_REGISTRY.get(name, {})
        return cls(name=name, config=config)