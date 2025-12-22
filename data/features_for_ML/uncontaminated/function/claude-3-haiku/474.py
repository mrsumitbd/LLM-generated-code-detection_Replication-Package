import numpy as np
from scipy.interpolate import RBFInterpolator

def create_nurbs_sphere_surface(num_points=50, radius=1.0):
    """
    Create a NURBS (Non-Uniform Rational B-Spline) sphere surface.

    Args:
        num_points (int): Number of points to generate on the sphere surface.
        radius (float): Radius of the sphere.

    Returns:
        tuple: (vertices, faces)
            vertices (numpy.ndarray): Array of vertex coordinates.
            faces (numpy.ndarray): Array of face indices.
    """
    # Generate points on a unit sphere
    theta = np.linspace(0, 2 * np.pi, num_points)
    phi = np.linspace(0, np.pi, num_points)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    x = np.cos(theta_grid) * np.sin(phi_grid)
    y = np.sin(theta_grid) * np.sin(phi_grid)
    z = np.cos(phi_grid)

    vertices = np.column_stack((x.flatten(), y.flatten(), z.flatten())) * radius

    # Create faces using a triangulation
    faces = []
    for i in range(num_points - 1):
        for j in range(num_points - 1):
            face1 = [i * num_points + j, i * num_points + j + 1, (i + 1) * num_points + j]
            face2 = [(i + 1) * num_points + j, i * num_points + j + 1, (i + 1) * num_points + j + 1]
            faces.append(face1)
            faces.append(face2)

    return np.array(vertices), np.array(faces)