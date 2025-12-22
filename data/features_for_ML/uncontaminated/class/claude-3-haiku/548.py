from enum import Enum
import torch

class PredictionType(Enum):
    EPSILON = 0
    V = 1

class NRS:

    @classmethod
    def INPUT_TYPES(cls):
        return [PredictionType.EPSILON, PredictionType.V]

    def _get_pred_type(self, model) -> PredictionType:
        if hasattr(model, 'predict_epsilon'):
            return PredictionType.EPSILON
        elif hasattr(model, 'predict_v'):
            return PredictionType.V
        else:
            raise ValueError("Model does not have a valid prediction type")

    def _convert_to_eps_space(self, x_orig, sig_root, sigma, cond, uncond):
        x_div = x_orig / sig_root
        x_eps = (x_div - uncond) / sigma
        return x_eps

    def _finalize_from_eps_space(self, x_orig, x_div, x_final, sig_root, sigma):
        x_rec = x_final * sigma + uncond
        x_out = x_rec * sig_root
        return x_out

    def _convert_to_v_space(self, x_orig, sig_root, sigma, cond, uncond):
        x_div = x_orig / sig_root
        x_v = (x_div - uncond) / sigma
        return x_v

    def _finalize_from_v_space(self, x_orig, x_div, x_final, sig_root, sigma):
        x_rec = x_final * sigma + uncond
        x_out = x_rec * sig_root
        return x_out

    def patch(self, model, skew, stretch, squash):
        pred_type = self._get_pred_type(model)
        if pred_type == PredictionType.EPSILON:
            model.predict_epsilon = lambda x, c, u: self._convert_to_eps_space(x, skew, stretch, c, u)
            model.finalize_from_epsilon = lambda x, xd, xf, s, ss: self._finalize_from_eps_space(x, xd, xf, s, ss)
        elif pred_type == PredictionType.V:
            model.predict_v = lambda x, c, u: self._convert_to_v_space(x, skew, stretch, c, u)
            model.finalize_from_v = lambda x, xd, xf, s, ss: self._finalize_from_v_space(x, xd, xf, s, ss)
        else:
            raise ValueError("Invalid prediction type")