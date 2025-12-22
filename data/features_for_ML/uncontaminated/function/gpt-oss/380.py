def rounded_corners(corner_string):
    parts = [p.strip() for p in corner_string.split(',')]
    return f"border-radius:{' '.join(f'{p}px' for p in parts)};"