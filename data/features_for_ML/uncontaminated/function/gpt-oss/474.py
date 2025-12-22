import math

def create_nurbs_sphere_surface():
    """
    Create a simple NURBS representation of a unit sphere.
    The surface is defined by a 4x4 grid of control points with
    uniform weights.  The knot vectors and degrees are chosen
    to produce a quadratic NURBS surface.
    """
    # Degrees
    degree_u = 2
    degree_v = 2

    # Knot vectors for a clamped quadratic NURBS
    knots_u = [0.0, 0.0, 1.0, 1.0]
    knots_v = [0.0, 0.0, 1.0, 1.0]

    # Control points grid (4x4) for a unit sphere
    # u: 0, pi/2, pi, 3pi/2
    # v: 0, pi/2, pi, 3pi/2
    # The points are computed using spherical coordinates.
    control_points = []
    weights = []

    u_angles = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]
    v_angles = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]

    for v in v_angles:
        row_cp = []
        row_wt = []
        for u in u_angles:
            x = math.cos(u) * math.sin(v)
            y = math.sin(u) * math.sin(v)
            z = math.cos(v)
            row_cp.append((x, y, z))
            # Uniform weight of 1 for all control points
            row_wt.append(1.0)
        control_points.append(row_cp)
        weights.append(row_wt)

    return {
        "control_points": control_points,
        "weights": weights,
        "knots_u": knots_u,
        "knots_v": knots_v,
        "degree_u": degree_u,
        "degree_v": degree_v,
    }