import numpy as np

def create_fisheye_camera(params, w, h):
    cx, cy, fx, fy, k1, k2, k3, k4 = params
    u, v = np.meshgrid(np.arange(w), np.arange(h))
    u = (u - cx) / fx
    v = (v - cy) / fy
    r = np.sqrt(u**2 + v**2)
    theta = np.arctan(r)
    theta_d = theta * (1 + k1 * theta**2 + k2 * theta**4 + k3 * theta**6 + k4 * theta**8)
    scale = theta_d / r
    u = u * scale
    v = v * scale
    u = u * fx + cx
    v = v * fy + cy
    return u, v