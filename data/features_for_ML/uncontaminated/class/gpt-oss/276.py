class CogVAEDecoderStateDictConverter:
    """
    Converter for CogVAE decoder state dictionaries between the Diffusers
    format and the Civitai format.

    The default implementation performs a no‑op conversion, but the class
    allows custom key mappings to be supplied if needed.
    """

    def __init__(self, diffusers_to_civitai_map=None, civitai_to_diffusers_map=None):
        """
        Parameters
        ----------
        diffusers_to_civitai_map : dict, optional
            Mapping from Diffusers key names to Civitai key names.
        civitai_to_diffusers_map : dict, optional
            Mapping from Civitai key names to Diffusers key names.
        """
        self.diffusers_to_civitai_map = diffusers_to_civitai_map or {}
        self.civitai_to_diffusers_map = civitai_to_diffusers_map or {}

    def from_diffusers(self, state_dict):
        """
        Convert a state dictionary from the Diffusers format to the Civitai format.

        Parameters
        ----------
        state_dict : dict
            The state dictionary in Diffusers format.

        Returns
        -------
        dict
            The converted state dictionary in Civitai format.
        """
        return {
            self.diffusers_to_civitai_map.get(k, k): v
            for k, v in state_dict.items()
        }

    def from_civitai(self, state_dict):
        """
        Convert a state dictionary from the Civitai format to the Diffusers format.

        Parameters
        ----------
        state_dict : dict
            The state dictionary in Civitai format.

        Returns
        -------
        dict
            The converted state dictionary in Diffusers format.
        """
        return {
            self.civitai_to_diffusers_map.get(k, k): v
            for k, v in state_dict.items()
        }