from PyQt5.QtWidgets import QMainWindow, QToolBar, QActionGroup
from PyQt5.QtGui import QAction, QIcon
from PyQt5.QtCore import Qt
from typing import Dict, Any, Callable
from app_state import AppState


class Toolbar:

    def __init__(self, main_window: QMainWindow, app_state: AppState, handlers: Dict[str, Callable]):
        self.main_window = main_window
        self.app_state = app_state
        self.handlers = handlers
        self.toolbar = None
        self.tool_buttons = {}
        self.action_group = None

    def create_toolbar(self) -> QToolBar:
        self.toolbar = QToolBar("Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(self.toolbar.iconSize())
        
        self._add_tool_group(self.toolbar)
        
        self.main_window.addToolBar(self.toolbar)
        return self.toolbar

    def _add_tool_group(self, toolbar: QToolBar):
        self.action_group = QActionGroup(toolbar)
        self.action_group.setExclusive(True)
        
        tools_config = [
            {
                "name": "selection",
                "icon": "selection.png",
                "tooltip": "Selection Tool",
                "shortcut": "S",
                "handler": "on_selection_tool"
            },
            {
                "name": "draw",
                "icon": "draw.png",
                "tooltip": "Draw Tool",
                "shortcut": "D",
                "handler": "on_draw_tool"
            },
            {
                "name": "erase",
                "icon": "erase.png",
                "tooltip": "Erase Tool",
                "shortcut": "E",
                "handler": "on_erase_tool"
            },
            {
                "name": "zoom",
                "icon": "zoom.png",
                "tooltip": "Zoom Tool",
                "shortcut": "Z",
                "handler": "on_zoom_tool"
            }
        ]
        
        for tool_config in tools_config:
            action = self._create_action(tool_config)
            self.action_group.addAction(action)
            toolbar.addAction(action)
            self.tool_buttons[tool_config["name"]] = action
        
        if self.tool_buttons:
            first_tool = list(self.tool_buttons.values())[0]
            first_tool.setChecked(True)

    def _create_action(self, data: Dict[str, Any], tooltip_prefix: str = "") -> QAction:
        action = QAction(self.main_window)
        
        if "icon" in data:
            try:
                icon = QIcon(f"resources/icons/{data['icon']}")
                action.setIcon(icon)
            except:
                pass
        
        if "tooltip" in data:
            tooltip_text = tooltip_prefix + data["tooltip"]
            if "shortcut" in data:
                tooltip_text += f" ({data['shortcut']})"
            action.setToolTip(tooltip_text)
        
        if "shortcut" in data:
            action.setShortcut(data["shortcut"])
        
        action.setCheckable(True)
        
        if "handler" in data and data["handler"] in self.handlers:
            handler = self.handlers[data["handler"]]
            action.triggered.connect(lambda checked=False, name=data.get("name"): self._handle_tool_action(name, handler))
        
        return action

    def _handle_tool_action(self, tool_name: str, handler: Callable):
        self._update_active_tool_button(tool_name)
        handler()

    def _update_active_tool_button(self, tool_name: str):
        if tool_name in self.tool_buttons:
            self.tool_buttons[tool_name].setChecked(True)
            self.app_state.set_active_tool(tool_name)