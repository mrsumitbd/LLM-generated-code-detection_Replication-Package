from cosmos_xenna._cosmos_xenna.pipelines.private.scheduling import data_structures as rust

class ProblemState:
    def __init__(self, stages: list[ProblemStageState]) -> None:
        self._r = rust.ProblemState([s.rust for s in stages])

    @property
    def rust(self) -> rust.ProblemState:
        return self._r