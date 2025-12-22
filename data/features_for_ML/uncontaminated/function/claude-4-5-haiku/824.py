def _get_focus_sign(self) -> tuple[str, str]:
    """
    Get the focus sign for GitHub Copilot VS Code extension.
    Reference Cursor's approach: click on the right panel first, then focus on input.

    Returns:
        Tuple of (JS script, target selector)
    """
    js_script = """
    (function() {
        // Click on the right panel first to ensure focus
        const rightPanel = document.querySelector('.copilot-panel, .chat-panel, [class*="panel"][class*="right"]');
        if (rightPanel) {
            rightPanel.click();
        }
        
        // Then focus on the input element
        const input = document.querySelector(
            'textarea[class*="input"], ' +
            'input[class*="chat"], ' +
            '.copilot-input, ' +
            '[class*="message-input"], ' +
            'textarea[placeholder*="Ask"], ' +
            'textarea'
        );
        if (input) {
            input.focus();
            return true;
        }
        return false;
    })();
    """
    
    target_selector = (
        'textarea[class*="input"], '
        'input[class*="chat"], '
        '.copilot-input, '
        '[class*="message-input"], '
        'textarea[placeholder*="Ask"], '
        'textarea'
    )
    
    return (js_script, target_selector)