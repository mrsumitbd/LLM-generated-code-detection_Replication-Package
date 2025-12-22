def derive_paths(cfg: PlotsConfig):
    paths = []
    for plot in cfg.plots:
        paths.append(os.path.join(cfg.output_dir, plot.filename))
    return paths