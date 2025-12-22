def _update_optional_panes_visibility(self):  # Identical to original logic
    """
    Updates the visibility of optional panes (e.g., Logs pane).

    Manages the grid layout and row weights to show or hide panes as configured.
    """
    # Get the configuration for optional panes visibility
    show_logs = getattr(self, 'show_logs_pane', True)
    
    # Update logs pane visibility
    if hasattr(self, 'logs_frame'):
        if show_logs:
            self.logs_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
            self.grid_rowconfigure(2, weight=1)
        else:
            self.logs_frame.grid_remove()
            self.grid_rowconfigure(2, weight=0)
    
    # Update any other optional panes similarly
    for pane_name in getattr(self, 'optional_panes', []):
        pane_attr = f'{pane_name}_frame'
        show_pane = getattr(self, f'show_{pane_name}_pane', True)
        
        if hasattr(self, pane_attr):
            pane = getattr(self, pane_attr)
            if show_pane:
                pane.grid()
            else:
                pane.grid_remove()
    
    # Refresh the layout
    self.update_idletasks()