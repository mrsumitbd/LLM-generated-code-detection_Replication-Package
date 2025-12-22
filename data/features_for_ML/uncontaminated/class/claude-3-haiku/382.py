import numpy as np
from typing import Union
from functools import cached_property
import torch

class MatrixGenerator:
    """Cayley graph generator that is square (n*n) integer matrix.

    This matrix applied (by multiplication) to n*m matrices.
    If `modulo != 0`, multiplication is modulo this number (`2<=modulo<=2^31`).
    If `modulo == 0`, multiplication is signed int64 multiplication with overflow.
    """

    def __init__(self, matrix: Union[list, np.ndarray], modulo: int = 0):
        self.matrix = np.array(matrix, dtype=np.int64)
        self.modulo = modulo

    def __post_init__(self):
        if self.modulo != 0:
            self.matrix = self.matrix % self.modulo

    def is_inverse_to(self, other: "MatrixGenerator") -> bool:
        return np.allclose(np.matmul(self.matrix, other.matrix), np.eye(self.n, dtype=np.int64))

    @cached_property
    def n(self):
        return self.matrix.shape[0]

    def apply(self, state: np.ndarray) -> np.ndarray:
        if self.modulo != 0:
            return np.matmul(self.matrix, state) % self.modulo
        else:
            return np.matmul(self.matrix, state)

    def apply_batch_torch(self, states: torch.Tensor) -> torch.Tensor:
        if self.modulo != 0:
            return torch.matmul(torch.from_numpy(self.matrix), states) % self.modulo
        else:
            return torch.matmul(torch.from_numpy(self.matrix), states)

    @cached_property
    def inv(self):
        return MatrixGenerator(np.linalg.inv(self.matrix).astype(np.int64), self.modulo)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, MatrixGenerator):
            return np.array_equal(self.matrix, other.matrix) and self.modulo == other.modulo
        return False

    @staticmethod
    def create(matrix: Union[list, np.ndarray], modulo: int = 0):
        return MatrixGenerator(matrix, modulo)