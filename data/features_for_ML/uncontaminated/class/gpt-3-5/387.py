class ControlNetFluxOutput:
    
    def __init__(self):
        self.weight = 0.0

    def apply_weight(self, weight: float):
        self.weight = weight

# Example usage
output = ControlNetFluxOutput()
output.apply_weight(0.5)
print(output.weight)