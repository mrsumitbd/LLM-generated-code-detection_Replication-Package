from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class GCGConfig:  # pylint: disable=too-many-instance-attributes
    """
    Configuration dataclass for the GCG attack parameters
    """
    num_classes: int
    num_channels: int
    image_size: Tuple[int, int]
    num_steps: int
    step_size: float
    random_start: bool
    norm_type: str
    norm_bound: float
    targeted: bool
    target_class: int
    loss_func: str
    confidence: float
    num_restarts: int = 1
    random_restarts: bool = False
    use_best_result: bool = True
    verbose: bool = False
    seed: int = 0
    device: str = "cpu"
    attack_type: str = "gcg"
    attack_name: str = "GCG"
    attack_description: str = "Generalized Carlini-Wagner Attack"
    attack_citation: str = "Carlini, N., & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In 2017 IEEE Symposium on Security and Privacy (SP) (pp. 39-57). IEEE."
    attack_url: str = "https://arxiv.org/abs/1608.04644"