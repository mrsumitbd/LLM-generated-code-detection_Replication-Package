class NeMoRLOpenAIChatRequestMixin:
    """
    Mixin that prepares the request parameters for an OpenAI chat request.
    It collects relevant attributes from the context object and stores them
    in a `request_params` dictionary for later use.
    """

    def model_post_init(self, context):
        """
        Populate the context with a dictionary of request parameters
        derived from its attributes. Only attributes that are present
        and not None are included.

        Parameters
        ----------
        context : object
            The context object that holds request configuration.
            Expected attributes include:
                - model (str)
                - messages (list)
                - temperature (float)
                - top_p (float)
                - max_tokens (int)
                - n (int)
                - stop (str or list)
                - presence_penalty (float)
                - frequency_penalty (float)
                - logit_bias (dict)
                - user (str)
        """
        # List of OpenAI chat request parameters to collect
        param_keys = [
            "model",
            "messages",
            "temperature",
            "top_p",
            "max_tokens",
            "n",
            "stop",
            "presence_penalty",
            "frequency_penalty",
            "logit_bias",
            "user",
        ]

        # Build the request_params dictionary
        request_params = {}
        for key in param_keys:
            value = getattr(context, key, None)
            if value is not None:
                request_params[key] = value

        # Attach the dictionary to the context for later use
        context.request_params = request_params