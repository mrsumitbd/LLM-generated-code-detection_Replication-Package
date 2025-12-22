from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ModelArgs:
    dim: int = 4096
    n_layers: int = 32
    n_heads: int = 32
    n_kv_heads: Optional[int] = None
    vocab_size: int = -1
    multiple_of: int = 256
    ffn_dim_multiplier: Optional[float] = None
    norm_eps: float = 1e-5
    rope_theta: float = 500000.0
    max_batch_size: int = 32
    max_seq_len: int = 2048
    device: str = "cuda"
    dtype: str = "bfloat16"

    def __post_init__(self):
        if self.n_kv_heads is None:
            self.n_kv_heads = self.n_heads
        if self.vocab_size == -1:
            self.vocab_size = 32000

    @classmethod
    def from_name(cls, name: str):
        model_configs = {
            "7B": cls(
                dim=4096,
                n_layers=32,
                n_heads=32,
                n_kv_heads=32,
                vocab_size=32000,
                multiple_of=256,
                ffn_dim_multiplier=None,
                norm_eps=1e-5,
                rope_theta=500000.0,
                max_batch_size=32,
                max_seq_len=2048,
            ),
            "13B": cls(
                dim=5120,
                n_layers=40,
                n_heads=40,
                n_kv_heads=40,
                vocab_size=32000,
                multiple_of=256,
                ffn_dim_multiplier=None,
                norm_eps=1e-5,
                rope_theta=500000.0,
                max_batch_size=32,
                max_seq_len=2048,
            ),
            "70B": cls(
                dim=8192,
                n_layers=80,
                n_heads=64,
                n_kv_heads=8,
                vocab_size=32000,
                multiple_of=256,
                ffn_dim_multiplier=None,
                norm_eps=1e-5,
                rope_theta=500000.0,
                max_batch_size=32,
                max_seq_len=2048,
            ),
        }
        if name not in model_configs:
            raise ValueError(f"Unknown model name: {name}")
        return model_configs[name]