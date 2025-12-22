def quaternion_to_axis_angle(w, x, y, z):
    import math
    
    angle = 2 * math.acos(w)
    s = math.sqrt(1 - w**2)
    
    if s < 0.001:
        axis = (x, y, z)
    else:
        axis = (x/s, y/s, z/s)
    
    return axis, angle