def _get_pages_selector(self) -> tuple[str, str]:
        """
        Get the pages selector for Cursor IDE.

        Returns:
            Tuple of (JS script, selector)
        """
        selector = 'div[autocapitalize="off"]'
        js_script = f"""
                   (() => {{
                       const el = document.querySelector('{selector}');
                       if (!el) return false;

                       el.focus();

                       const selection = window.getSelection();
                       const range = document.createRange();

                       range.selectNodeContents(el);
                       range.collapse(true);

                       selection.removeAllRanges();
                       selection.addRange(range);

                       return true;
                   }})();
                   """
        return js_script, selector