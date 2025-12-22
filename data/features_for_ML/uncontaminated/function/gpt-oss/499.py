import math
from typing import Iterable, Sequence, Tuple, Union

try:
    import numpy as np
except ImportError:
    np = None


def _to_np(arr):
    """Convert input to a NumPy array if possible, otherwise keep as list."""
    if np is None:
        return arr
    return np.asarray(arr, dtype=float)


def _normalize(v):
    """Return a unit vector of v. If v is zero, return zero vector."""
    norm = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if norm == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / norm, v[1] / norm, v[2] / norm)


def compute_vertex_normal(*args, **kwargs):
    """
    Compute the normal vector at a given vertex of a triangular mesh.

    Parameters
    ----------
    vertices : Sequence[Sequence[float]] or np.ndarray
        Array of vertex coordinates of shape (N, 3).
    faces : Sequence[Sequence[int]] or np.ndarray
        Array of face indices of shape (M, 3). Each row contains indices into
        the vertices array.
    vertex_index : int
        Index of the vertex for which the normal is computed.
    normalize : bool, optional
        If True (default), the resulting normal is normalized to unit length.
    weights : Sequence[float], optional
        Optional per-face weights. If provided, must have length equal to the
        number of faces. If omitted, face area is used as weight.

    Returns
    -------
    normal : Tuple[float, float, float]
        The computed normal vector. If the vertex is isolated (no adjacent
        faces), returns (0.0, 0.0, 0.0).

    Notes
    -----
    The normal is computed as the weighted average of the normals of all
    faces that contain the vertex. The weight defaults to the area of the
    face, but a custom weight can be supplied via the ``weights`` keyword.
    """
    # Parse positional arguments
    if len(args) >= 3:
        vertices, faces, vertex_index = args[:3]
        kwargs.update(args[3:])
    else:
        vertices = kwargs.pop("vertices", None)
        faces = kwargs.pop("faces", None)
        vertex_index = kwargs.pop("vertex_index", None)

    if vertices is None or faces is None or vertex_index is None:
        raise ValueError(
            "Missing required arguments: vertices, faces, and vertex_index must be provided."
        )

    normalize_flag = kwargs.pop("normalize", True)
    custom_weights = kwargs.pop("weights", None)

    # Convert to numpy arrays if available
    if np is not None:
        vertices = _to_np(vertices)
        faces = _to_np(faces)
        if custom_weights is not None:
            custom_weights = _to_np(custom_weights)
    else:
        # If numpy is not available, work with plain lists
        vertices = list(map(lambda p: (float(p[0]), float(p[1]), float(p[2])), vertices))
        faces = list(map(lambda f: (int(f[0]), int(f[1]), int(f[2])), faces))
        if custom_weights is not None:
            custom_weights = list(map(float, custom_weights))

    # Find all faces that include the vertex
    adjacent_faces = []
    for i, f in enumerate(faces):
        if vertex_index in f:
            adjacent_faces.append((i, f))

    if not adjacent_faces:
        return (0.0, 0.0, 0.0)

    normal_sum = [0.0, 0.0, 0.0]
    total_weight = 0.0

    for idx, f in adjacent_faces:
        # Retrieve vertex coordinates
        v0 = vertices[f[0]]
        v1 = vertices[f[1]]
        v2 = vertices[f[2]]

        # Compute face normal (not normalized)
        if np is not None:
            e1 = v1 - v0
            e2 = v2 - v0
            face_normal = np.cross(e1, e2)
            area = 0.5 * np.linalg.norm(face_normal)
            if area == 0:
                continue
            weight = custom_weights[idx] if custom_weights is not None else area
            normal_sum[0] += face_normal[0] * weight
            normal_sum[1] += face_normal[1] * weight
            normal_sum[2] += face_normal[2] * weight
            total_weight += weight
        else:
            # Manual cross product
            e1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
            e2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
            face_normal = (
                e1[1] * e2[2] - e1[2] * e2[1],
                e1[2] * e2[0] - e1[0] * e2[2],
                e1[0] * e2[1] - e1[1] * e2[0],
            )
            area = 0.5 * math.sqrt(
                face_normal[0] ** 2 + face_normal[1] ** 2 + face_normal[2] ** 2
            )
            if area == 0:
                continue
            weight = custom_weights[idx] if custom_weights is not None else area
            normal_sum[0] += face_normal[0] * weight
            normal_sum[1] += face_normal[1] * weight
            normal_sum[2] += face_normal[2] * weight
            total_weight += weight

    if total_weight == 0:
        return (0.0, 0.0, 0.0)

    # Average normal
    avg_normal = (
        normal_sum[0] / total_weight,
        normal_sum[1] / total_weight,
        normal_sum[2] / total_weight,
    )

    if normalize_flag:
        return _normalize(avg_normal)
    else:
        return avg_normal