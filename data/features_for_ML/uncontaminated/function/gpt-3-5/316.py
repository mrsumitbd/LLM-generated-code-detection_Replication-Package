def load_detector_by_name(detector_name, *, resize=1024, weights_path=None):
    if detector_name == 'ssd':
        return SSDObjectDetector(resize=resize, weights_path=weights_path)
    elif detector_name == 'yolo':
        return YOLOObjectDetector(resize=resize, weights_path=weights_path)
    else:
        raise ValueError("Unknown detector name: {}".format(detector_name))