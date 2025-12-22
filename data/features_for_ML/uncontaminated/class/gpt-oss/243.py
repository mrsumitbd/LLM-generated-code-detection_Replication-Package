class SD3TextEncoder1StateDictConverter:
    """
    Converter for SD3 Text Encoder 1 state dictionaries between the
    Diffusers and CivitAI formats.

    The Diffusers format prefixes all keys with ``text_encoder.`` while
    the CivitAI format prefixes them with ``model.``.  This converter
    removes those prefixes so that the resulting dictionary can be
    loaded directly into a PyTorch model that expects the unprefixed
    keys.
    """

    def __init__(self):
        # No state is required for this converter.
        pass

    def _strip_prefix(self, state_dict, prefix):
        """
        Internal helper that removes a given prefix from all keys in a
        state dictionary.  Keys that do not start with the prefix are
        left untouched.
        """
        new_state = {}
        for k, v in state_dict.items():
            if k.startswith(prefix):
                new_key = k[len(prefix) :]
            else:
                new_key = k
            new_state[new_key] = v
        return new_state

    def from_diffusers(self, state_dict):
        """
        Convert a Diffusers state dictionary to the format expected by
        the SD3 Text Encoder 1 model.

        Parameters
        ----------
        state_dict : dict
            State dictionary from a Diffusers checkpoint.

        Returns
        -------
        dict
            State dictionary with the ``text_encoder.`` prefix removed.
        """
        return self._strip_prefix(state_dict, "text_encoder.")

    def from_civitai(self, state_dict):
        """
        Convert a CivitAI state dictionary to the format expected by
        the SD3 Text Encoder 1 model.

        Parameters
        ----------
        state_dict : dict
            State dictionary from a CivitAI checkpoint.

        Returns
        -------
        dict
            State dictionary with the ``model.`` prefix removed.
        """
        return self._strip_prefix(state_dict, "model.")