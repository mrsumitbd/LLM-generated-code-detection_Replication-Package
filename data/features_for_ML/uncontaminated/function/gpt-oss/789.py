import numpy as np

def _compute_statistics(x, m, dim=2, eps=None):
    """
    Compute weighted means and covariances for a Gaussian mixture model.

    Parameters
    ----------
    x : ndarray, shape (N, D)
        Data points.
    m : ndarray, shape (N, K)
        Responsibility matrix (weights) for each component.
    dim : int, optional
        Dimension along which to compute statistics.  Only ``dim==2`` is
        supported (samples are rows, features are columns).  The argument
        is kept for API compatibility.
    eps : float, optional
        Small value added to the diagonal of each covariance matrix for
        numerical stability.  If ``None`` the function will use a default
        of ``1e-6``.

    Returns
    -------
    mu : ndarray, shape (K, D)
        Weighted means of each component.
    cov : ndarray, shape (K, D, D)
        Weighted covariances of each component.
    """
    if eps is None:
        eps = 1e-6

    # Ensure we are working with numpy arrays
    x = np.asarray(x, dtype=np.float64)
    m = np.asarray(m, dtype=np.float64)

    # Basic shape checks
    if x.ndim != 2:
        raise ValueError(f"x must be 2‑D, got shape {x.shape}")
    if m.ndim != 2:
        raise ValueError(f"m must be 2‑D, got shape {m.shape}")
    if x.shape[0] != m.shape[0]:
        raise ValueError("Number of samples in x and m must match")

    N, D = x.shape
    K = m.shape[1]

    # Sum of responsibilities for each component
    Nk = m.sum(axis=0)  # shape (K,)

    # Avoid division by zero
    Nk_safe = np.where(Nk == 0, 1.0, Nk)

    # Weighted means
    mu = (m.T @ x) / Nk_safe[:, None]  # shape (K, D)

    # Weighted covariances
    cov = np.empty((K, D, D), dtype=np.float64)
    for k in range(K):
        # Difference from mean
        diff = x - mu[k]  # (N, D)
        # Weighted outer product
        weighted = diff.T * m[:, k]  # (D, N)
        cov_k = weighted @ diff / Nk_safe[k]  # (D, D)
        # Add small value to diagonal for numerical stability
        cov_k += eps * np.eye(D, dtype=np.float64)
        cov[k] = cov_k

    return mu, cov