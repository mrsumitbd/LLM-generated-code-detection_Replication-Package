def broadcast_params(module):
    for param in module.parameters():
        param.requires_grad = False