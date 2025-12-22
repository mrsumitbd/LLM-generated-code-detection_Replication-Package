class MockCompletion:
    """
    A lightweight mock for an OpenAI‑style completion endpoint.
    It records every call and returns pre‑configured responses.
    """

    def __init__(self):
        # Queue of responses to return on each call
        self._responses = []
        # History of calls: list of (prompt, kwargs) tuples
        self._history = []

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------
    def set_responses(self, responses):
        """Replace the entire response queue with the given iterable."""
        self._responses = list(responses)

    def add_response(self, response):
        """Append a single response to the queue."""
        self._responses.append(response)

    def reset(self):
        """Clear the response queue and call history."""
        self._responses.clear()
        self._history.clear()

    # ------------------------------------------------------------------
    # Call interface
    # ------------------------------------------------------------------
    def complete(self, prompt, **kwargs):
        """
        Simulate a completion call.

        Parameters
        ----------
        prompt : str
            The prompt sent to the model.
        **kwargs : dict
            Additional arguments that would normally be passed to the API.

        Returns
        -------
        dict
            A minimal OpenAI‑style response containing the next queued
            response text.
        """
        self._history.append((prompt, kwargs))

        if not self._responses:
            raise RuntimeError("MockCompletion: no responses left in the queue")

        response_text = self._responses.pop(0)
        return {"choices": [{"text": response_text}]}

    # Allow the instance to be called directly
    __call__ = complete

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------
    def get_call_history(self):
        """Return a copy of the call history."""
        return list(self._history)

    def get_remaining_responses(self):
        """Return a copy of the remaining queued responses."""
        return list(self._responses)