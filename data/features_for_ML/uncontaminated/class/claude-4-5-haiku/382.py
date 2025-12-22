class MatrixGenerator:
    """Cayley graph generator that is square (n*n) integer matrix.

    This matrix applied (by multiplication) to n*m matrices.
    If `modulo != 0`, multiplication is modulo this number (`2<=modulo<=2^31`).
    If `modulo == 0`, multiplication is signed int64 multiplication with overflow.
    """

    def __init__(self, matrix: np.ndarray, modulo: int = 0):
        self.matrix = np.asarray(matrix, dtype=np.int64)
        self.modulo = modulo
        self.__post_init__()

    @staticmethod
    def create(matrix: Union[list, np.ndarray], modulo: int = 0):
        return MatrixGenerator(matrix, modulo)

    def __post_init__(self):
        if self.matrix.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
        if self.matrix.shape[0] != self.matrix.shape[1]:
            raise ValueError("Matrix must be square")
        if self.modulo != 0 and (self.modulo < 2 or self.modulo > 2**31):
            raise ValueError("modulo must be 0 or in range [2, 2^31]")

    def is_inverse_to(self, other: "MatrixGenerator") -> bool:
        if self.n != other.n or self.modulo != other.modulo:
            return False
        
        product = self._matrix_multiply(self.matrix, other.matrix)
        identity = np.eye(self.n, dtype=np.int64)
        
        return np.array_equal(product, identity)

    @cached_property
    def n(self):
        return self.matrix.shape[0]

    def apply(self, state: np.ndarray) -> np.ndarray:
        state = np.asarray(state, dtype=np.int64)
        result = self.matrix @ state
        
        if self.modulo != 0:
            result = result % self.modulo
        else:
            result = np.asarray(result, dtype=np.int64)
        
        return result

    def apply_batch_torch(self, states: torch.Tensor) -> torch.Tensor:
        matrix_torch = torch.from_numpy(self.matrix).to(states.device).to(states.dtype)
        result = torch.matmul(matrix_torch, states)
        
        if self.modulo != 0:
            result = result % self.modulo
        
        return result

    @cached_property
    def inv(self):
        try:
            inv_matrix = np.linalg.inv(self.matrix)
            
            if self.modulo != 0:
                inv_matrix = np.round(inv_matrix).astype(np.int64)
                inv_matrix = inv_matrix % self.modulo
            else:
                inv_matrix = np.round(inv_matrix).astype(np.int64)
            
            inv_gen = MatrixGenerator(inv_matrix, self.modulo)
            
            if self.is_inverse_to(inv_gen):
                return inv_gen
            else:
                return None
        except np.linalg.LinAlgError:
            return None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MatrixGenerator):
            return False
        return (np.array_equal(self.matrix, other.matrix) and 
                self.modulo == other.modulo)

    def _matrix_multiply(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        result = a @ b
        if self.modulo != 0:
            result = result % self.modulo
        else:
            result = np.asarray(result, dtype=np.int64)
        return result