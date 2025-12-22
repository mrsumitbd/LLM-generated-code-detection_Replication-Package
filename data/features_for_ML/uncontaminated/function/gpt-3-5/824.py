def _get_focus_sign(self) -> tuple[str, str]:
    js_script = """
    const focusSign = document.createElement('div');
    focusSign.id = 'focus-sign-copilot';
    focusSign.style.position = 'fixed';
    focusSign.style.top = '0';
    focusSign.style.left = '0';
    focusSign.style.width = '100%';
    focusSign.style.height = '100%';
    focusSign.style.zIndex = '9999';
    focusSign.style.pointerEvents = 'none';
    focusSign.style.background = 'rgba(255, 255, 255, 0.5)';
    document.body.appendChild(focusSign);
    """

    target_selector = '#focus-sign-copilot'

    return js_script, target_selector