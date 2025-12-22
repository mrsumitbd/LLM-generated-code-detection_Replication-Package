def derive_paths(cfg: PlotsConfig):
    """Derive and set paths in the PlotsConfig object based on base_path and plot names."""
    if not hasattr(cfg, 'base_path') or cfg.base_path is None:
        raise ValueError("base_path must be set in PlotsConfig")
    
    base_path = Path(cfg.base_path)
    
    if hasattr(cfg, 'plots') and cfg.plots:
        for plot in cfg.plots:
            if hasattr(plot, 'name') and plot.name:
                plot_path = base_path / plot.name
                if hasattr(plot, 'path'):
                    plot.path = str(plot_path)
                else:
                    setattr(plot, 'path', str(plot_path))
    
    if hasattr(cfg, 'output_dir'):
        output_path = base_path / 'output'
        cfg.output_dir = str(output_path)
    
    return cfg