from typing import Any, Optional, Tuple, Union

class GCGConfig:  # pylint: disable=too-many-instance-attributes
    """
    Configuration dataclass for the GCG attack parameters
    """

    num_steps: int = 250
    optim_str_init: Union[str, list[str]] = "x x x x x x x x x x x x x x x x x x x x"
    search_width: int = 512
    batch_size: Optional[int] = None
    topk: int = 256
    n_replace: int = 1
    buffer_size: int = 0
    use_mellowmax: bool = False
    mellowmax_alpha: float = 1.0
    early_stop: bool = False
    allow_non_ascii: bool = False
    filter_ids: bool = True
    add_space_before_target: Union[dict[str, bool], bool] = True
    # NanoGCG does not use a space when setting up the optimization,
    # but then does use one in the example script for attacking a model.
    # This seems inconsistent: explicitly use a config option for it.
    add_space_before_opt_string: bool = False
    seed: Optional[int] = None
    verbosity: str = "INFO"
    output_path: str = "./"
    input_path: Optional[str] = None
    config_options: Optional[dict] = None
    model_stack: tuple[str, ...] = ("core",)