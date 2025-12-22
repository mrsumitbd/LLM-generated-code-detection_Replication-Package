class SDUNetStateDictConverter:
    """
    A simple converter that rewrites state‑dict keys between the
    Diffusers and Civitai naming conventions for SDU‑Net models.
    """

    def __init__(self, custom_mapping=None):
        """
        Parameters
        ----------
        custom_mapping : dict, optional
            A dictionary that maps old key fragments to new ones.
            If provided, it will be merged with the default mappings.
        """
        # Default mappings for Diffusers → Civitai
        self._diff_to_civitai = {
            "diffusion_model": "model",
            "input_blocks": "input",
            "middle_block": "middle",
            "output_blocks": "output",
            "time_embed": "time",
            "norm": "norm",
            "conv": "conv",
            "proj": "proj",
            "to_out": "out",
        }

        # Default mappings for Civitai → Diffusers
        self._civitai_to_diff = {
            "model": "diffusion_model",
            "input": "input_blocks",
            "middle": "middle_block",
            "output": "output_blocks",
            "time": "time_embed",
            "norm": "norm",
            "conv": "conv",
            "proj": "proj",
            "out": "to_out",
        }

        if custom_mapping:
            # Merge custom mapping into the defaults
            self._diff_to_civitai.update(custom_mapping.get("diff_to_civitai", {}))
            self._civitai_to_diff.update(custom_mapping.get("civitai_to_diff", {}))

    def _convert_keys(self, state_dict, mapping):
        """
        Internal helper that applies a key mapping to a state dict.
        """
        new_state = {}
        for key, value in state_dict.items():
            new_key = key
            for old, new in mapping.items():
                new_key = new_key.replace(old, new)
            new_state[new_key] = value
        return new_state

    def from_diffusers(self, state_dict):
        """
        Convert a Diffusers state dict to the Civitai format.

        Parameters
        ----------
        state_dict : dict
            The original Diffusers state dict.

        Returns
        -------
        dict
            A new state dict with keys rewritten for Civitai.
        """
        return self._convert_keys(state_dict, self._diff_to_civitai)

    def from_civitai(self, state_dict):
        """
        Convert a Civitai state dict to the Diffusers format.

        Parameters
        ----------
        state_dict : dict
            The original Civitai state dict.

        Returns
        -------
        dict
            A new state dict with keys rewritten for Diffusers.
        """
        return self._convert_keys(state_dict, self._civitai_to_diff)