class ProblemState:

    def __init__(self, stages: list[ProblemStageState]) -> None:
        self._stages = stages

    @property
    def rust(self) -> rust.ProblemState:
        return rust.ProblemState([stage.rust for stage in self._stages])