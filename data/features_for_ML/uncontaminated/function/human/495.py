import torch

def center_size(boxes):
    """ Convert prior_boxes to (cx, cy, w, h)
    representation for comparison to center-size form ground truth data.
    Args:
        boxes: (tensor) point_form boxes
    Return:
        boxes: (tensor) Converted xmin, ymin, xmax, ymax form of boxes.
    """
    return torch.cat(
        (boxes[:, 2:] + boxes[:, :2]) / 2,  # cx, cy
        boxes[:, 2:] - boxes[:, :2],
        1)  # w, h