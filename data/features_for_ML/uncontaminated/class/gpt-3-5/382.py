from typing import Union, Any
import numpy as np
import torch
from cached_property import cached_property

class MatrixGenerator:
    """Cayley graph generator that is square (n*n) integer matrix.

    This matrix applied (by multiplication) to n*m matrices.
    If `modulo != 0`, multiplication is modulo this number (`2<=modulo<=2^31`).
    If `modulo == 0`, multiplication is signed int64 multiplication with overflow.
    """

    def __init__(self, matrix: np.ndarray, modulo: int = 0):
        self.matrix = matrix
        self.modulo = modulo

    @staticmethod
    def create(matrix: Union[list, np.ndarray], modulo: int = 0):
        return MatrixGenerator(np.array(matrix), modulo)

    @cached_property
    def n(self):
        return self.matrix.shape[0]

    def apply(self, state: np.ndarray) -> np.ndarray:
        if self.modulo != 0:
            return np.dot(state, self.matrix) % self.modulo
        else:
            return np.dot(state, self.matrix)

    def apply_batch_torch(self, states: torch.Tensor) -> torch.Tensor:
        if self.modulo != 0:
            return torch.matmul(states, torch.tensor(self.matrix)) % self.modulo
        else:
            return torch.matmul(states, torch.tensor(self.matrix))

    @cached_property
    def inv(self):
        if self.modulo != 0:
            return np.linalg.inv(self.matrix) % self.modulo
        else:
            return np.linalg.inv(self.matrix)

    def is_inverse_to(self, other: "MatrixGenerator") -> bool:
        return np.array_equal(self.matrix @ other.matrix % self.modulo, np.eye(self.n, dtype=int) % self.modulo)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MatrixGenerator):
            return False
        return np.array_equal(self.matrix, other.matrix) and self.modulo == other.modulo