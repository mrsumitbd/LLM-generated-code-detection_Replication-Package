import types
from enum import Enum
from typing import Any, Dict, Tuple


class PredictionType(Enum):
    EPSILON = "epsilon"
    V = "v"
    MODEL_OUTPUT = "model_output"


class NRS:
    @classmethod
    def INPUT_TYPES(s) -> Dict[str, Any]:
        """
        Return a dictionary describing the input types for the NRS node.
        """
        return {
            "skew": {"type": "float", "default": 1.0},
            "stretch": {"type": "float", "default": 1.0},
            "squash": {"type": "float", "default": 1.0},
        }

    def _get_pred_type(self, model) -> PredictionType:
        """
        Determine the prediction type of the model.
        """
        # Try to read a prediction_type attribute; fall back to EPSILON
        pred_type = getattr(model, "prediction_type", None)
        if isinstance(pred_type, str):
            try:
                return PredictionType(pred_type.lower())
            except ValueError:
                pass
        return PredictionType.EPSILON

    def _convert_to_eps_space(
        self,
        x_orig: Any,
        sig_root: Any,
        sigma: Any,
        cond: Any,
        uncond: Any,
    ) -> Any:
        """
        Convert the model output to epsilon space.
        """
        # Simple linear interpolation between conditioned and unconditioned
        return (cond - uncond) * sigma + uncond

    def _finalize_from_eps_space(
        self,
        x_orig: Any,
        x_div: Any,
        x_final: Any,
        sig_root: Any,
        sigma: Any,
    ) -> Any:
        """
        Finalize the output after epsilon space conversion.
        """
        # In this simplified implementation we just return the final value
        return x_final

    def _convert_to_v_space(
        self,
        x_orig: Any,
        sig_root: Any,
        sigma: Any,
        cond: Any,
        uncond: Any,
    ) -> Any:
        """
        Convert the model output to v space.
        """
        # v = epsilon * sigma
        eps = (cond - uncond) * sigma + uncond
        return eps * sigma

    def _finalize_from_v_space(
        self,
        x_orig: Any,
        x_div: Any,
        x_final: Any,
        sig_root: Any,
        sigma: Any,
    ) -> Any:
        """
        Finalize the output after v space conversion.
        """
        return x_final

    def patch(self, model, skew: float = 1.0, stretch: float = 1.0, squash: float = 1.0):
        """
        Patch the model's forward method to apply skew, stretch, and squash.
        """
        original_forward = model.forward

        def patched_forward(*args, **kwargs):
            out = original_forward(*args, **kwargs)
            # Apply simple scaling transformations
            out = out * skew
            out = out * stretch
            out = out / (1.0 + squash * (out ** 2))
            return out

        model.forward = types.MethodType(patched_forward, model)
        return model