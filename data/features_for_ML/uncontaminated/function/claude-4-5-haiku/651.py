def lr_lambda(current_step):
    return 1.0 / (1.0 + 0.05 * current_step)