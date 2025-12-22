class RetrievalConfig:
    """Configuration for BM25 retrieval parameters"""

    def __init__(self, k1: float = 1.5, b: float = 0.75, k3: float = 500.0):
        self.k1 = k1
        self.b = b
        self.k3 = k3

    @property
    def k1(self) -> float:
        return self._k1

    @k1.setter
    def k1(self, value: float):
        if value <= 0:
            raise ValueError("k1 must be positive")
        self._k1 = float(value)

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, value: float):
        if not 0 <= value <= 1:
            raise ValueError("b must be in [0, 1]")
        self._b = float(value)

    @property
    def k3(self) -> float:
        return self._k3

    @k3.setter
    def k3(self, value: float):
        if value < 0:
            raise ValueError("k3 must be non‑negative")
        self._k3 = float(value)

    def bm25_score(
        self,
        tf: int,
        doc_len: int,
        avg_doc_len: float,
        idf: float,
        query_tf: int = 1,
    ) -> float:
        """
        Compute the BM25 score for a single term.

        Parameters
        ----------
        tf : int
            Term frequency in the document.
        doc_len : int
            Length of the document (number of terms).
        avg_doc_len : float
            Average document length in the collection.
        idf : float
            Inverse document frequency of the term.
        query_tf : int, default 1
            Term frequency in the query.

        Returns
        -------
        float
            BM25 relevance score.
        """
        if tf < 0 or doc_len <= 0 or avg_doc_len <= 0 or idf < 0 or query_tf < 0:
            raise ValueError("All frequency and length parameters must be non‑negative, "
                             "and doc_len/avg_doc_len must be positive")

        denom = tf + self.k1 * (1 - self.b + self.b * doc_len / avg_doc_len)
        term1 = (self.k1 + 1) * tf / denom if denom != 0 else 0.0

        denom_q = query_tf + self.k3
        term2 = (self.k3 + 1) * query_tf / denom_q if denom_q != 0 else 0.0

        return idf * term1 * term2

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(k1={self.k1!r}, "
            f"b={self.b!r}, k3={self.k3!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RetrievalConfig):
            return NotImplemented
        return (
            self.k1 == other.k1
            and self.b == other.b
            and self.k3 == other.k3
        )