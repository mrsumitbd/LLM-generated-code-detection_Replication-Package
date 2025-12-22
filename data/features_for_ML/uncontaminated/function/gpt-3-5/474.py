import numpy as np
import math
import scipy.special

def create_nurbs_sphere_surface(radius=1, num_points=30):
    u = np.linspace(0, 2 * np.pi, num_points)
    v = np.linspace(-np.pi/2, np.pi/2, num_points)
    u, v = np.meshgrid(u, v)
    
    x = radius * np.cos(v) * np.cos(u)
    y = radius * np.cos(v) * np.sin(u)
    z = radius * np.sin(v)
    
    weights = np.ones_like(x)
    
    return x, y, z, weights