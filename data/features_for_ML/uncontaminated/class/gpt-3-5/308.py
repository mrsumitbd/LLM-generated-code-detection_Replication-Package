import rust

class ProblemState:

    def __init__(self, stages: list[ProblemStageState]) -> None:
        self.stages = stages

    @property
    def rust(self) -> rust.ProblemState:
        return rust.ProblemState(self.stages)