import numpy as np
import torch
from .camera_models import (
    OpenCVFisheyeCameraModelParameters,
    OpenCVPinholeCameraModelParameters,
    ShutterType,
    image_points_to_camera_rays,
    pixels_to_image_points,
)
from .utils import (
    compute_max_radius,
    create_camera_visualization,
    get_center_and_diag,
    get_worker_id,
    pinhole_camera_rays,
    qvec_to_so3,
    read_colmap_extrinsics_binary,
    read_colmap_extrinsics_text,
    read_colmap_intrinsics_binary,
    read_colmap_intrinsics_text,
)

def create_fisheye_camera(params, w, h):
            # Generate UV coordinates
            u = np.tile(np.arange(w), h)
            v = np.arange(h).repeat(w)
            out_shape = (1, h, w, 3)
            resolution = np.array([w, h]).astype(np.int64)
            principal_point = params[2:4].astype(np.float32)
            focal_length = params[0:2].astype(np.float32)
            radial_coeffs = params[4:].astype(np.float32)
            # Estimate max angle for fisheye
            max_radius_pixels = compute_max_radius(resolution.astype(np.float64), principal_point)
            fov_angle_x = 2.0 * max_radius_pixels / focal_length[0]
            fov_angle_y = 2.0 * max_radius_pixels / focal_length[1]
            max_angle = np.max([fov_angle_x, fov_angle_y]) / 2.0

            params = OpenCVFisheyeCameraModelParameters(
                principal_point=principal_point,
                focal_length=focal_length,
                radial_coeffs=radial_coeffs,
                resolution=resolution,
                max_angle=max_angle,
                shutter_type=ShutterType.GLOBAL,
            )
            pixel_coords = torch.tensor(np.stack([u, v], axis=1), dtype=torch.int32)
            image_points = pixels_to_image_points(pixel_coords)
            rays_d_cam = image_points_to_camera_rays(params, image_points)
            rays_o_cam = torch.zeros_like(rays_d_cam)
            return (
                params.to_dict(),
                rays_o_cam.to(torch.float32).reshape(out_shape),
                rays_d_cam.to(torch.float32).reshape(out_shape),
                type(params).__name__,
            )