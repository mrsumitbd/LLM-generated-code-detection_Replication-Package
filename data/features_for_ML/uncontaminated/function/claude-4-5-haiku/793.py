def create_fisheye_camera(params, w, h):
    """
    Create a fisheye camera projection.
    
    Args:
        params: Camera parameters (focal length, principal point, distortion coefficients)
        w: Image width
        h: Image height
    
    Returns:
        A function that projects 3D points to 2D fisheye image coordinates
    """
    import numpy as np
    
    # Extract camera parameters
    if isinstance(params, dict):
        fx = params.get('fx', 1.0)
        fy = params.get('fy', 1.0)
        cx = params.get('cx', w / 2)
        cy = params.get('cy', h / 2)
        k1 = params.get('k1', 0.0)
        k2 = params.get('k2', 0.0)
    else:
        # Assume params is a tuple/list: (fx, fy, cx, cy, k1, k2)
        fx, fy, cx, cy = params[:4] if len(params) >= 4 else (1.0, 1.0, w/2, h/2)
        k1 = params[4] if len(params) > 4 else 0.0
        k2 = params[5] if len(params) > 5 else 0.0
    
    def project_point(point_3d):
        """Project a 3D point to 2D fisheye image coordinates."""
        x, y, z = point_3d
        
        # Avoid division by zero
        if z == 0:
            return None
        
        # Normalize coordinates
        x_norm = x / z
        y_norm = y / z
        
        # Calculate radius in normalized image plane
        r = np.sqrt(x_norm**2 + y_norm**2)
        
        # Apply fisheye distortion (using atan model)
        # theta = atan(r)
        theta = np.arctan(r)
        
        # Apply radial distortion coefficients
        theta_d = theta * (1 + k1 * theta**2 + k2 * theta**4)
        
        # Avoid division by zero
        if r == 0:
            x_dist = 0
            y_dist = 0
        else:
            # Scale back to image plane
            scale = theta_d / r
            x_dist = x_norm * scale
            y_dist = y_norm * scale
        
        # Apply focal length and principal point
        u = fx * x_dist + cx
        v = fy * y_dist + cy
        
        return (u, v)
    
    def generate_uv_coordinates():
        """Generate UV coordinates for the fisheye camera."""
        uv_coords = np.zeros((h, w, 2), dtype=np.float32)
        for y in range(h):
            for x in range(w):
                uv_coords[y, x] = [x, y]
        return uv_coords
    
    # Return both the projection function and UV coordinate generator
    return {
        'project': project_point,
        'generate_uv': generate_uv_coordinates,
        'params': {
            'fx': fx,
            'fy': fy,
            'cx': cx,
            'cy': cy,
            'k1': k1,
            'k2': k2,
            'width': w,
            'height': h
        }
    }