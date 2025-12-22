class ControlNetFluxOutput:

    def __init__(self, output: torch.Tensor = None):
        self.output = output

    def apply_weight(self, weight: float):
        if self.output is not None:
            self.output = self.output * weight
        return self