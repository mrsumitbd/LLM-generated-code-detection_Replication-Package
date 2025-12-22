from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction
from typing import Dict, Any

class Toolbar:

    def __init__(self, main_window: QMainWindow, app_state: AppState, handlers: Dict[str, callable]):
        self.main_window = main_window
        self.app_state = app_state
        self.handlers = handlers

    def create_toolbar(self) -> QToolBar:
        toolbar = QToolBar()
        self._add_tool_group(toolbar)
        return toolbar

    def _add_tool_group(self, toolbar: QToolBar):
        for tool_name, handler in self.handlers.items():
            action_data = {"name": tool_name, "handler": handler}
            action = self._create_action(action_data)
            toolbar.addAction(action)

    def _create_action(self, data: Dict[str, Any], tooltip_prefix: str = "") -> QAction:
        action = QAction(data["name"], self.main_window)
        action.triggered.connect(data["handler"])
        action.setToolTip(tooltip_prefix + data["name"])
        return action

    def _update_active_tool_button(self, tool_name: str):
        for action in self.main_window.findChildren(QAction):
            if action.text() == tool_name:
                action.setChecked(True)
            else:
                action.setChecked(False)