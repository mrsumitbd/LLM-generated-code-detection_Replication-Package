def build_roboflow(image_set, args, resolution):
    roboflow_config = {
        "image_set": image_set,
        "args": args,
        "resolution": resolution
    }
    return roboflow_config