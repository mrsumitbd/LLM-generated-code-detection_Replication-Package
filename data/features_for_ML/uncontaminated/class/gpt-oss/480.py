from typing import Dict, Any, Callable
from PyQt5.QtWidgets import QToolBar, QAction, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Toolbar:
    """
    A toolbar that hosts a set of tool actions. Each action is created from a
    dictionary of data and is connected to a handler supplied by the caller.
    The toolbar keeps the active tool highlighted based on the application
    state.
    """

    def __init__(self, main_window: QMainWindow, app_state: Any, handlers: Dict[str, Callable]):
        """
        Parameters
        ----------
        main_window : QMainWindow
            The main window to which the toolbar will be added.
        app_state : Any
            An object that exposes an ``active_tool`` attribute or property.
        handlers : Dict[str, Callable]
            Mapping from tool names to callables that will be invoked when the
            corresponding action is triggered.
        """
        self.main_window = main_window
        self.app_state = app_state
        self.handlers = handlers
        self._actions: Dict[str, QAction] = {}
        self.toolbar = self.create_toolbar()

    def create_toolbar(self) -> QToolBar:
        """
        Create the toolbar, populate it with actions and add it to the main
        window.

        Returns
        -------
        QToolBar
            The created toolbar.
        """
        toolbar = QToolBar("Tools", self.main_window)
        toolbar.setIconSize(Qt.QSize(24, 24))
        self._add_tool_group(toolbar)
        self.main_window.addToolBar(Qt.TopToolBarArea, toolbar)
        return toolbar

    def _add_tool_group(self, toolbar: QToolBar):
        """
        Add a group of tool actions to the toolbar. Each action is created
        from the handlers dictionary. The data for each action is expected to
        be a dictionary containing at least a ``name`` key and optionally
        ``icon``, ``text``, ``shortcut`` and ``tooltip`` keys.

        Parameters
        ----------
        toolbar : QToolBar
            The toolbar to which the actions will be added.
        """
        for tool_name, handler in self.handlers.items():
            # Build a minimal data dictionary for the action
            data: Dict[str, Any] = {
                "name": tool_name,
                "text": tool_name.replace("_", " ").title(),
                "icon": None,
                "shortcut": None,
                "tooltip": f"Activate {tool_name}",
            }
            action = self._create_action(data)
            action.triggered.connect(handler)
            action.setCheckable(True)
            toolbar.addAction(action)
            self._actions[tool_name] = action

        # Ensure the active tool is highlighted initially
        self._update_active_tool_button(self.app_state.active_tool)

    def _create_action(self, data: Dict[str, Any], tooltip_prefix: str = "") -> QAction:
        """
        Create a QAction from the provided data dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary containing action metadata. Expected keys:
            - ``name`` (str): unique identifier for the action.
            - ``text`` (str): display text.
            - ``icon`` (str or QIcon): path to an icon file or a QIcon instance.
            - ``shortcut`` (str): keyboard shortcut.
            - ``tooltip`` (str): tooltip text.
        tooltip_prefix : str, optional
            Prefix to prepend to the tooltip.

        Returns
        -------
        QAction
            The created action.
        """
        name = data.get("name", "")
        text = data.get("text", "")
        icon_data = data.get("icon")
        shortcut = data.get("shortcut")
        tooltip = data.get("tooltip", "")

        action = QAction(text, self.main_window)

        if icon_data:
            if isinstance(icon_data, QIcon):
                action.setIcon(icon_data)
            else:
                action.setIcon(QIcon(icon_data))

        if shortcut:
            action.setShortcut(shortcut)

        action.setToolTip(f"{tooltip_prefix}{tooltip}")
        action.setStatusTip(text)

        return action

    def _update_active_tool_button(self, tool_name: str):
        """
        Update the checked state of all tool actions so that only the action
        corresponding to ``tool_name`` is checked.

        Parameters
        ----------
        tool_name : str
            The name of the tool that should be active.
        """
        for name, action in self._actions.items():
            action.setChecked(name == tool_name)