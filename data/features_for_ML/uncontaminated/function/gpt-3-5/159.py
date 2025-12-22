def from_pretrained(model_config):
    model = Model()
    model.load_state_dict(torch.load(model_config['model_path']))
    model.eval()
    return model