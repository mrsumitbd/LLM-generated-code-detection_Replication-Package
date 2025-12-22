def init_weights(m, mean=0.0, std=0.01):
    return torch.normal(mean=mean, std=std, size=(m,))