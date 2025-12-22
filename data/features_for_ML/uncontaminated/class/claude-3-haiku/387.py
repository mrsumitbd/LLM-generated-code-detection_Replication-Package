class ControlNetFluxOutput:
    def __init__(self, flux_output: float, weight: float = 1.0):
        self.flux_output = flux_output
        self.weight = weight

    def apply_weight(self, weight: float):
        self.weight = weight
        self.weighted_flux_output = self.flux_output * self.weight