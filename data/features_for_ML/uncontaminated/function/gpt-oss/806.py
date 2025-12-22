import os
from pathlib import Path
from typing import Any

def derive_paths(cfg: Any) -> Any:
    """
    Derive missing directory paths in a PlotsConfig instance.

    The function inspects the configuration object for the following
    attributes and, if they are missing or empty, derives them from
    the base directory.  It also ensures that the derived directories
    exist on disk.

    Expected attributes (case-sensitive):
        - base_dir   : The root directory for all derived paths.
        - plots_dir  : Directory where plot files are stored.
        - output_dir : Directory for output files.
        - data_dir   : Directory for raw data.
        - log_dir    : Directory for log files.
        - fig_dir    : Directory for figure files (subdirectory of plots_dir).

    Parameters
    ----------
    cfg : Any
        A configuration object (typically a dataclass or simple object)
        that contains at least a `base_dir` attribute.

    Returns
    -------
    Any
        The same configuration object with derived attributes set.
    """
    # Helper to get attribute safely
    def get_attr(name: str) -> Any:
        return getattr(cfg, name, None)

    # Ensure base_dir is present
    base_dir = get_attr("base_dir")
    if not base_dir:
        raise ValueError("Configuration must contain a non-empty 'base_dir' attribute.")
    base_dir = Path(base_dir).expanduser().resolve()

    # Derive plots_dir
    plots_dir = get_attr("plots_dir")
    if not plots_dir:
        plots_dir = base_dir / "plots"
        setattr(cfg, "plots_dir", str(plots_dir))
    else:
        plots_dir = Path(plots_dir).expanduser().resolve()

    # Derive output_dir
    output_dir = get_attr("output_dir")
    if not output_dir:
        output_dir = base_dir / "output"
        setattr(cfg, "output_dir", str(output_dir))
    else:
        output_dir = Path(output_dir).expanduser().resolve()

    # Derive data_dir
    data_dir = get_attr("data_dir")
    if not data_dir:
        data_dir = base_dir / "data"
        setattr(cfg, "data_dir", str(data_dir))
    else:
        data_dir = Path(data_dir).expanduser().resolve()

    # Derive log_dir
    log_dir = get_attr("log_dir")
    if not log_dir:
        log_dir = base_dir / "logs"
        setattr(cfg, "log_dir", str(log_dir))
    else:
        log_dir = Path(log_dir).expanduser().resolve()

    # Derive fig_dir (subdirectory of plots_dir)
    fig_dir = get_attr("fig_dir")
    if not fig_dir:
        fig_dir = plots_dir / "figures"
        setattr(cfg, "fig_dir", str(fig_dir))
    else:
        fig_dir = Path(fig_dir).expanduser().resolve()

    # Ensure all derived directories exist
    for d in (plots_dir, output_dir, data_dir, log_dir, fig_dir):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            raise OSError(f"Failed to create directory '{d}': {exc}") from exc

    return cfg