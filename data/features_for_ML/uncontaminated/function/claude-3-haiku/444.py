def check_optimizer_groups(optimizer_groups):
    if not isinstance(optimizer_groups, list):
        return False

    for group in optimizer_groups:
        if not isinstance(group, dict):
            return False

        if 'params' not in group or not isinstance(group['params'], list):
            return False

        if 'lr' not in group or not isinstance(group['lr'], (int, float)):
            return False

        if 'weight_decay' not in group or not isinstance(group['weight_decay'], (int, float)):
            return False

    return True