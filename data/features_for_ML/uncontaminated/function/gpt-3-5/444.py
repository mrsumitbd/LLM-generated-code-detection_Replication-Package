def check_optimizer_groups(optimizer_groups):
    for group in optimizer_groups:
        if not isinstance(group, list):
            return False
        for optimizer in group:
            if not callable(optimizer):
                return False
    return True