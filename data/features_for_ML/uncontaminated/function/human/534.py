from typing import Any, Dict, List, Optional
from jrdev.ui.ui import PrintType, terminal_print

def _handle_get(app: Any, args: List[str], manager: Any) -> None:
    # Get model for a specific profile
    if len(args) < 3:
        app.ui.print_text(
            "Missing profile name. Usage: /modelprofile get [profile]",
            PrintType.ERROR,
        )
        return

    profile = args[2]
    model = manager.get_model(profile)
    app.ui.print_text(f"Profile '{profile}' uses model: {model}", PrintType.INFO)