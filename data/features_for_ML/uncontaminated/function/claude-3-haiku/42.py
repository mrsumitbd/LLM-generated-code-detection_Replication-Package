def lr_lambda(current_step):
    import math
    
    initial_lr = 0.001
    decay_rate = 0.1
    decay_steps = 1000
    
    lr = initial_lr * (decay_rate ** (current_step / decay_steps))
    
    return lr