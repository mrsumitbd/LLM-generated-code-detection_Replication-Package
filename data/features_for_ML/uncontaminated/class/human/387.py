import torch

class ControlNetFluxOutput:
    single_block_residuals: list[torch.Tensor] | None
    double_block_residuals: list[torch.Tensor] | None

    def apply_weight(self, weight: float):
        if self.single_block_residuals is not None:
            for i in range(len(self.single_block_residuals)):
                self.single_block_residuals[i] = self.single_block_residuals[i] * weight
        if self.double_block_residuals is not None:
            for i in range(len(self.double_block_residuals)):
                self.double_block_residuals[i] = self.double_block_residuals[i] * weight