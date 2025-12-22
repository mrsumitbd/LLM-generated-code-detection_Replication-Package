class NRS:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "skew": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "stretch": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.01}),
                "squash": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.01}),
            }
        }

    def _get_pred_type(self, model) -> PredictionType:
        if hasattr(model, 'model_type'):
            model_type = model.model_type
            if model_type == "eps":
                return PredictionType.EPSILON
            elif model_type == "v_prediction":
                return PredictionType.V_PREDICTION
            elif model_type == "x0":
                return PredictionType.X0
        return PredictionType.EPSILON

    def _convert_to_eps_space(self, x_orig, sig_root, sigma, cond, uncond):
        return x_orig

    def _finalize_from_eps_space(self, x_orig, x_div, x_final, sig_root, sigma):
        return x_final

    def _convert_to_v_space(self, x_orig, sig_root, sigma, cond, uncond):
        return x_orig

    def _finalize_from_v_space(self, x_orig, x_div, x_final, sig_root, sigma):
        return x_final

    def patch(self, model, skew, stretch, squash):
        return (model,)