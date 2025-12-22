def _update_optional_panes_visibility(self):
    for pane in self.optional_panes:
        if pane.is_visible():
            pane.grid(row=0, column=0, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            break
    else:
        self.grid_rowconfigure(0, weight=0)