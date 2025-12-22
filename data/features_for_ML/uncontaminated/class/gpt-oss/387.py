class ControlNetFluxOutput:
    """
    A simple container for ControlNet flux output data that can be scaled by a weight.
    The data can be any numeric type that supports multiplication by a float (e.g. int, float,
    list/tuple of numbers, numpy array, torch tensor, etc.).
    """

    def __init__(self, data):
        """
        Initialize the container with the given data.

        Parameters
        ----------
        data : numeric, list/tuple of numeric, or array-like
            The output data to be stored.
        """
        self.data = data

    def apply_weight(self, weight: float):
        """
        Scale the stored data by the given weight.

        Parameters
        ----------
        weight : float
            The factor by which to scale the data.

        Returns
        -------
        ControlNetFluxOutput
            The instance itself, after scaling the data.
        """
        # Try to use the data's own multiplication if possible
        try:
            self.data = self.data * weight
        except Exception:
            # Fallback for plain iterables (list/tuple)
            if isinstance(self.data, (list, tuple)):
                self.data = [x * weight for x in self.data]
            else:
                raise TypeError(
                    f"Unsupported data type {type(self.data)} for weight application"
                )
        return self

    def __repr__(self):
        return f"{self.__class__.__name__}(data={self.data!r})"