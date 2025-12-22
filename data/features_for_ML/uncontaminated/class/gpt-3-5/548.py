from enum import Enum

class PredictionType(Enum):
    CONDITIONAL = 1
    UNCONDITIONAL = 2

class NRS:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'skew': float,
            'stretch': float,
            'squash': float
        }

    def _get_pred_type(self, model) -> PredictionType:
        # Implementation not provided
        pass

    def _convert_to_eps_space(self, x_orig, sig_root, sigma, cond, uncond):
        # Implementation not provided
        pass

    def _finalize_from_eps_space(self, x_orig, x_div, x_final, sig_root, sigma):
        # Implementation not provided
        pass

    def _convert_to_v_space(self, x_orig, sig_root, sigma, cond, uncond):
        # Implementation not provided
        pass

    def _finalize_from_v_space(self, x_orig, x_div, x_final, sig_root, sigma):
        # Implementation not provided
        pass

    def patch(self, model, skew, stretch, squash):
        # Implementation not provided
        pass