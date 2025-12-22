import numpy as np
import torch
from functools import cached_property
from typing import Any, Union

class MatrixGenerator:
    """Cayley graph generator that is square (n*n) integer matrix.

    This matrix applied (by multiplication) to n*m matrices.
    If `modulo != 0`, multiplication is modulo this number (`2<=modulo<=2^31`).
    If `modulo == 0`, multiplication is signed int64 multiplication with overflow.
    """

    def __init__(self, matrix: np.ndarray, modulo: int = 0):
        self.matrix = matrix
        self.modulo = modulo
        self.__post_init__()

    @staticmethod
    def create(matrix: Union[list, np.ndarray], modulo: int = 0):
        """Create a MatrixGenerator from a list or ndarray."""
        mat = np.array(matrix, dtype=np.int64)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise ValueError("Matrix must be square.")
        if modulo != 0 and not (2 <= modulo <= 2**31):
            raise ValueError("Modulo must be 0 or in [2, 2^31].")
        return MatrixGenerator(mat, modulo)

    def __post_init__(self):
        # Ensure matrix is int64
        self.matrix = self.matrix.astype(np.int64)

    def is_inverse_to(self, other: "MatrixGenerator") -> bool:
        """Check if this matrix is the inverse of `other`."""
        if self.n != other.n or self.modulo != other.modulo:
            return False
        prod = self.apply(other.matrix)
        # Build identity
        I = np.eye(self.n, dtype=np.int64)
        if self.modulo != 0:
            prod = prod % self.modulo
            I = I % self.modulo
        return np.array_equal(prod, I)

    @cached_property
    def n(self):
        return self.matrix.shape[0]

    def apply(self, state: np.ndarray) -> np.ndarray:
        """Apply the matrix to a state (n*m or n,) ndarray."""
        state = np.array(state, dtype=np.int64)
        if state.ndim == 1:
            if state.shape[0] != self.n:
                raise ValueError("State dimension mismatch.")
            res = self.matrix @ state
        else:
            if state.shape[0] != self.n:
                raise ValueError("State dimension mismatch.")
            res = self.matrix @ state
        if self.modulo != 0:
            res = res % self.modulo
        return res

    def apply_batch_torch(self, states: torch.Tensor) -> torch.Tensor:
        """Apply the matrix to a batch of states (batch, n, m) or (batch, n)."""
        mat_torch = torch.from_numpy(self.matrix).to(states.device, dtype=states.dtype)
        if states.ndim == 2:
            # (batch, n)
            res = torch.matmul(mat_torch, states.t()).t()
        else:
            # (batch, n, m)
            res = torch.matmul(mat_torch, states)
        if self.modulo != 0:
            res = res % self.modulo
        return res

    @cached_property
    def inv(self):
        """Return the inverse matrix (modulo if applicable)."""
        # Compute inverse over float, round, cast to int64
        inv_float = np.linalg.inv(self.matrix.astype(np.float64))
        inv_int = np.rint(inv_float).astype(np.int64)
        if self.modulo != 0:
            inv_int = inv_int % self.modulo
        return inv_int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MatrixGenerator):
            return False
        return self.modulo == other.modulo and np.array_equal(self.matrix, other.matrix)