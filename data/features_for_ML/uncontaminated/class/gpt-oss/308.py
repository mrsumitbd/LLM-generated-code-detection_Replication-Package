from __future__ import annotations

from typing import List

# Assume these are defined elsewhere in the project
# from .problem_stage_state import ProblemStageState
# from . import rust

class ProblemState:
    """
    Represents the state of a problem consisting of multiple stages.
    """

    def __init__(self, stages: List["ProblemStageState"]) -> None:
        """
        Initialize a ProblemState with a list of stages.

        Parameters
        ----------
        stages : list[ProblemStageState]
            The stages that make up this problem state.
        """
        self.stages = stages

    @property
    def rust(self) -> "rust.ProblemState":
        """
        Convert the Python representation to the corresponding Rust struct.

        Returns
        -------
        rust.ProblemState
            The Rust representation of this problem state.
        """
        # Each stage is expected to expose a `rust` property that returns its Rust counterpart.
        rust_stages = [stage.rust for stage in self.stages]
        return rust.ProblemState(stages=rust_stages)