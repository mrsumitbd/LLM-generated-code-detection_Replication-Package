from config_and_logger import logger

def _update_optional_panes_visibility(self):  # Identical to original logic
        """
        Updates the visibility of optional panes (e.g., Logs pane).

        Manages the grid layout and row weights to show or hide panes as configured.
        """

        if not hasattr(self, "main_content_frame") or not self.main_content_frame.winfo_exists():
            logger.error(
                "GUI",
                "_update_optional_panes_visibility",
                "main_content_frame not found.",
            )
            return
        if not hasattr(self, "log_frame") or not self.log_frame.winfo_exists():
            logger.error("GUI", "_update_optional_panes_visibility", "log_frame not found.")
            return
        logs_are_visible = self.logs_visible_var.get()
        if logs_are_visible:
            if not self.log_frame.winfo_ismapped():
                self.log_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=(5, 0))
            self.main_content_frame.grid_rowconfigure(0, weight=3)
            self.main_content_frame.grid_rowconfigure(1, weight=0)  # Panels toolbar
            self.main_content_frame.grid_rowconfigure(2, weight=0)  # Transcription panel
            self.main_content_frame.grid_rowconfigure(3, weight=1)  # Log panel
        else:
            if self.log_frame.winfo_ismapped():
                self.log_frame.grid_forget()
            self.main_content_frame.grid_rowconfigure(0, weight=1)
            self.main_content_frame.grid_rowconfigure(1, weight=0)  # Panels toolbar
            self.main_content_frame.grid_rowconfigure(2, weight=0)  # Transcription panel
            self.main_content_frame.grid_rowconfigure(3, weight=0)  # Log panel