def _update_optional_panes_visibility(self):
    """
    Updates the visibility of optional panes (e.g., Logs pane).

    Manages the grid layout and row weights to show or hide panes as configured.
    """
    # Determine the parent container that owns the grid rows.
    parent = getattr(self, "main_frame", self)

    # Build a list of optional panes if not already present.
    if not hasattr(self, "optional_panes"):
        optional_panes = []
        # Look for attributes that look like panes (ending with "_pane").
        for attr_name in dir(self):
            if attr_name.endswith("_pane"):
                frame = getattr(self, attr_name, None)
                if frame is None:
                    continue
                # Ensure the object is a Tkinter widget with grid_info.
                try:
                    grid_info = frame.grid_info()
                except Exception:
                    continue
                row = grid_info.get("row")
                if row is None:
                    continue
                # Build a config key that is expected to control visibility.
                config_key = f"show_{attr_name}"
                optional_panes.append(
                    {"frame": frame, "config_key": config_key, "row": row}
                )
        self.optional_panes = optional_panes

    # Retrieve the configuration dictionary or object.
    config = getattr(self, "config", {})
    # Helper to get a boolean value from the config.
    def get_bool(key, default=True):
        if isinstance(config, dict):
            return bool(config.get(key, default))
        # If config is an object with a get method.
        try:
            return bool(config.get(key, default))
        except Exception:
            return default

    # Iterate over each optional pane and adjust its visibility.
    for pane in getattr(self, "optional_panes", []):
        frame = pane["frame"]
        row = pane["row"]
        config_key = pane["config_key"]

        # Determine whether the pane should be shown.
        show = get_bool(config_key, True)

        if show:
            # If the frame is not currently mapped, grid it.
            if not frame.winfo_ismapped():
                # Place it in the correct row; keep existing column and sticky.
                grid_info = frame.grid_info()
                col = grid_info.get("column", 0)
                sticky = grid_info.get("sticky", "nsew")
                frame.grid(row=row, column=col, sticky=sticky)
            # Give the row a positive weight so it expands.
            parent.grid_rowconfigure(row, weight=1)
        else:
            # If the frame is mapped, remove it from the grid.
            if frame.winfo_ismapped():
                frame.grid_remove()
            # Remove weight so the row does not expand.
            parent.grid_rowconfigure(row, weight=0)