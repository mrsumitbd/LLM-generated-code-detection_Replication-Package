def resize_landmark(landmark, w, h, new_w, new_h):
    new_landmark = []
    for x, y in landmark:
        new_x = x * new_w / w
        new_y = y * new_h / h
        new_landmark.append((new_x, new_y))
    return new_landmark