def _get_focus_sign(self) -> tuple[str, str]:
    """
    Get the focus sign for GitHub Copilot VS Code extension.
    Reference Cursor's approach: click on the right panel first, then focus on input.

    Returns:
        Tuple of (JS script, target selector)
    """
    # JavaScript that clicks the Copilot panel (if present) and then focuses the input field.
    script = """
    (function () {
        // Try to click the Copilot panel to bring it into view
        const panel = document.querySelector('.copilot-panel');
        if (panel) {
            panel.click();
        }
        // Focus the input area inside the Copilot panel
        const input = document.querySelector('.copilot-input');
        if (input) {
            input.focus();
        }
    })();
    """
    # The selector for the input element that we want to focus on
    selector = ".copilot-input"
    return script, selector