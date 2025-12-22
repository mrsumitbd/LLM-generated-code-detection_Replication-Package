import numpy as np
from functools import cached_property
from typing import Optional, Union, Any
import torch

class MatrixGenerator:
    """Cayley graph generator that is square (n*n) integer matrix.

    This matrix applied (by multiplication) to n*m matrices.
    If `modulo != 0`, multiplication is modulo this number (`2<=modulo<=2^31`).
    If `modulo == 0`, multiplication is signed int64 multiplication with overflow.
    """

    matrix: np.ndarray
    modulo: int

    @staticmethod
    def create(matrix: Union[list, np.ndarray], modulo: int = 0):
        matrix = np.array(matrix, dtype=np.int64)
        if modulo > 0:
            matrix %= modulo
        return MatrixGenerator(matrix, modulo)

    def __post_init__(self):
        # Validation.
        assert self.matrix.shape == (self.n, self.n), "Must be square matrix"
        assert self.matrix.dtype == np.int64
        if self.modulo != 0:
            assert 2 <= self.modulo <= 2**31
            assert self.matrix.min() >= 0
            assert self.matrix.max() < self.modulo

    def is_inverse_to(self, other: "MatrixGenerator") -> bool:
        if self.modulo != other.modulo:
            return False
        eye = np.eye(self.n, dtype=np.int64)
        return np.array_equal(self.apply(other.matrix), eye) and np.array_equal(other.apply(self.matrix), eye)

    @cached_property
    def n(self):
        return self.matrix.shape[0]

    def apply(self, state: np.ndarray) -> np.ndarray:
        """Multiplies (from left) this matrix by a n*m matrix."""
        ans = self.matrix @ state
        if self.modulo > 0:
            ans %= self.modulo
        return ans

    def apply_batch_torch(self, states: torch.Tensor) -> torch.Tensor:
        """Multiplies (from left) this matrix by a batch of n*m torch Tensors."""
        assert len(states.shape) == 3
        assert states.shape[1] == self.n
        mx = torch.tensor(self.matrix, dtype=torch.int64, device=states.device)
        mx = mx.unsqueeze(0).unsqueeze(-1)
        ans = (mx * states.unsqueeze(1)).sum(dim=2)
        if self.modulo > 0:
            ans %= self.modulo
        return ans

    @cached_property
    def inv(self):
        """Inverse of this matrix. Throws error if matrix is not invertible."""
        # TODO: implement modular inverse, if needed.
        matrix_inv = np.array(np.linalg.inv(self.matrix), dtype=np.int64)
        assert np.array_equal(self.apply(matrix_inv), np.eye(self.n)), "Matrix is not invertible."
        return MatrixGenerator.create(matrix_inv, self.modulo)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MatrixGenerator):
            return False
        return self.modulo == other.modulo and np.array_equal(self.matrix, other.matrix)