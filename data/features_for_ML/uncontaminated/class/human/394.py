from datasets import load_dataset
from nemo_rl.data.interfaces import TaskDataSpec

class HelpSteer3Dataset:
    """HelpSteer3 preference dataset for DPO training."""

    def __init__(self) -> None:
        ds = load_dataset("nvidia/HelpSteer3", "preference")
        self.formatted_ds = ds.map(to_preference_data_format)

        self.task_spec = TaskDataSpec(
            task_name="HelpSteer3",
        )