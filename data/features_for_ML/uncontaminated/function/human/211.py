import os
from rich import print as rprint
from rich.console import Console

def print_logo():
    try:
        from rich import print as rprint
        from rich.console import Console

        console = Console()

        if console.color_system and not os.getenv("NO_COLOR"):
            tree_art = _get_pine_tree_art()
            text_art = _get_pyne_text_art()

            rprint("")

            # Print tree and text side by side
            max_lines = max(len(tree_art), len(text_art))
            for i in range(max_lines):
                tree_line = tree_art[i] if i < len(tree_art) else ""
                text_line = text_art[i - 1] if i >= 1 and (i - 1) < len(text_art) else ""

                # Combine tree and text with proper spacing
                combined_line = f"{tree_line:<40} {text_line}"
                rprint(combined_line)
        else:
            raise ImportError  # Force the except block

    except (UnicodeEncodeError, ImportError):
        plain_text = _get_plain_text_art()
        for line in plain_text:
            print(line)