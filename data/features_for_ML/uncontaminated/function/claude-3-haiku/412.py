def _update_optional_panes_visibility(self):
    # Get the current visibility state of the optional panes
    logs_pane_visible = self.logs_pane.isVisible()
    other_pane_visible = self.other_pane.isVisible()

    # Determine the new visibility state based on the configuration
    if self.config.show_logs_pane:
        self.logs_pane.setVisible(True)
    else:
        self.logs_pane.setVisible(False)

    if self.config.show_other_pane:
        self.other_pane.setVisible(True)
    else:
        self.other_pane.setVisible(False)

    # Update the grid layout and row weights to accommodate the new visibility state
    if logs_pane_visible != self.logs_pane.isVisible() or other_pane_visible != self.other_pane.isVisible():
        self.grid_layout.setRowStretch(0, 1 if self.logs_pane.isVisible() else 0)
        self.grid_layout.setRowStretch(1, 1 if self.other_pane.isVisible() else 0)
        self.grid_layout.setRowStretch(2, 1 if self.logs_pane.isVisible() or self.other_pane.isVisible() else 0)