def _get_focus_sign(self) -> tuple[str, str]:
    """
    Get the focus sign for GitHub Copilot VS Code extension.
    Reference Cursor's approach: click on the right panel first, then focus on input.

    Returns:
        Tuple of (JS script, target selector)
    """
    js_script = """
        const rightPanel = document.querySelector('.side-panel.right');
        rightPanel.click();

        const inputField = document.querySelector('input.input-field');
        inputField.focus();
    """
    target_selector = 'input.input-field'
    return js_script, target_selector