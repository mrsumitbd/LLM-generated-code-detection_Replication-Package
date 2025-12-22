import numpy as np

class linear1:
    """
    A simple linear (fully‑connected) layer.

    Parameters
    ----------
    in_features : int
        Number of input features.
    out_features : int, optional
        Number of output features. If not provided, defaults to `in_features`.
    bias : bool, optional
        If True, adds a learnable bias to the output.
    """

    def __init__(self, in_features, out_features=None, bias=True):
        if out_features is None:
            out_features = in_features
        self.in_features = int(in_features)
        self.out_features = int(out_features)
        self.bias_flag = bool(bias)

        # Weight matrix of shape (out_features, in_features)
        self.weight = np.random.randn(self.out_features, self.in_features)

        # Bias vector of shape (out_features,)
        self.bias = np.random.randn(self.out_features) if self.bias_flag else None

    def forward(self, x):
        """
        Compute the linear transformation.

        Parameters
        ----------
        x : np.ndarray
            Input array of shape (..., in_features).

        Returns
        -------
        np.ndarray
            Transformed array of shape (..., out_features).
        """
        x = np.asarray(x)
        if x.shape[-1] != self.in_features:
            raise ValueError(
                f"Expected last dimension to be {self.in_features}, got {x.shape[-1]}"
            )
        out = x @ self.weight.T
        if self.bias_flag:
            out += self.bias
        return out

    def __call__(self, x):
        return self.forward(x)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(in_features={self.in_features}, "
            f"out_features={self.out_features}, bias={self.bias_flag})"
        )