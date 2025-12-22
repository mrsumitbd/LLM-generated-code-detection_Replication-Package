from typing import Dict, Any
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction
from PyQt5.QtGui import QIcon
from app_state import AppState

class Toolbar:

    def __init__(self, main_window: QMainWindow, app_state: AppState, handlers: Dict[str, callable]):
        self.main_window = main_window
        self.app_state = app_state
        self.handlers = handlers
        self.toolbar = self.create_toolbar()
        self.main_window.addToolBar(self.toolbar)

    def create_toolbar(self) -> QToolBar:
        toolbar = QToolBar()
        self._add_tool_group(toolbar)
        return toolbar

    def _add_tool_group(self, toolbar: QToolBar):
        for tool_data in self.app_state.tools:
            action = self._create_action(tool_data)
            toolbar.addAction(action)

    def _create_action(self, data: Dict[str, Any], tooltip_prefix: str = "") -> QAction:
        action = QAction(QIcon(data["icon"]), data["label"], self.main_window)
        action.setCheckable(True)
        action.setChecked(data["name"] == self.app_state.active_tool)
        action.triggered.connect(lambda checked: self._update_active_tool_button(data["name"]))
        action.triggered.connect(self.handlers[data["name"]])
        action.setToolTip(f"{tooltip_prefix}{data['tooltip']}")
        return action

    def _update_active_tool_button(self, tool_name: str):
        self.app_state.active_tool = tool_name
        for action in self.toolbar.actions():
            action.setChecked(action.text() == self.app_state.active_tool)