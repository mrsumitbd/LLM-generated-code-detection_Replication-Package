class ProblemState:
    def __init__(self, stages: list[ProblemStageState]) -> None:
        self._stages = stages

    @property
    def rust(self) -> rust.ProblemState:
        rust_stages = [stage.rust for stage in self._stages]
        return rust.ProblemState(rust_stages)