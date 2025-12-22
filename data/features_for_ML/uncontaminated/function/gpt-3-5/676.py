import numpy as np

def amplitude_to_db(
    S,
    *,
    ref: float | Callable = 1.0,
    amin: float = 1e-5,
    top_db: float | None = 80.0,
) -> np.floating[Any] | np.ndarray:
    return 20.0 * np.log10(np.maximum(amin, np.abs(S)) / np.maximum(amin, ref))