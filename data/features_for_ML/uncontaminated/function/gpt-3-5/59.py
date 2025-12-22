def replace_ls(old_ls: TIMMLayerScale):
    new_ls = TIMMLayerScale()
    new_ls.ls = old_ls.ls
    new_ls.lsml = old_ls.lsml
    new_ls.lsd = old_ls.lsd
    new_ls.lsdm = old_ls.lsdm
    new_ls.lsdch = old_ls.lsdch
    new_ls.lsdmch = old_ls.lsdmch
    return new_ls