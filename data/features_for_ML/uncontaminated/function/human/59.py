from timm.models.vision_transformer import LayerScale as TIMMLayerScale

def replace_ls(old_ls: TIMMLayerScale):
        new_ls = Dinov2LayerScale(old_ls.gamma.shape[0], inplace=old_ls.inplace)
        new_ls.load_state_dict(old_ls.state_dict())
        return new_ls