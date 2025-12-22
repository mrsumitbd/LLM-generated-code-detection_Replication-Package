def lr_lambda(current_step):
    total_steps = 1000
    return max(0.0, 1.0 - current_step / total_steps)