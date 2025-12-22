import numpy as np

def compute_vertex_normal(*args, **kwargs):
    """
    Computes the vertex normal for a given set of vertices and faces.

    Args:
        *args: Variable-length argument list containing the following:
            - vertices (np.ndarray): A 2D numpy array of shape (N, 3) representing the vertex coordinates.
            - faces (np.ndarray): A 2D numpy array of shape (M, 3) representing the face indices.
        **kwargs: Keyword arguments (optional):
            - smooth (bool): If True, computes smooth vertex normals; otherwise, computes flat normals. Default is True.

    Returns:
        np.ndarray: A 2D numpy array of shape (N, 3) representing the computed vertex normals.
    """
    vertices, faces = args
    smooth = kwargs.get('smooth', True)

    # Compute face normals
    v1 = vertices[faces[:, 0]]
    v2 = vertices[faces[:, 1]]
    v3 = vertices[faces[:, 2]]
    face_normals = np.cross(v2 - v1, v3 - v1)
    face_normals /= np.linalg.norm(face_normals, axis=1, keepdims=True)

    if smooth:
        # Compute smooth vertex normals
        vertex_normals = np.zeros_like(vertices)
        for i, face in enumerate(faces):
            vertex_normals[face] += face_normals[i]
        vertex_normals /= np.linalg.norm(vertex_normals, axis=1, keepdims=True)
    else:
        # Compute flat vertex normals
        vertex_normals = face_normals[np.repeat(np.arange(len(faces)), 3)]

    return vertex_normals