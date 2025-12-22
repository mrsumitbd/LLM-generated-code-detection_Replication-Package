def _get_focus_sign(self) -> tuple[str, str]:
        """
        Get the focus sign for GitHub Copilot VS Code extension.
        Reference Cursor's approach: click on the right panel first, then focus on input.

        Returns:
            Tuple of (JS script, target selector)
        """
        target_selector = ".interactive-input-part"
        focus_js = f"""
               (() => {{
                    const editorContainer = document.querySelector('.interactive-input-editor');
                      if (!editorContainer) {{
                        return false;
                      }}
                      const monacoEditor = editorContainer.querySelector('.monaco-editor');
                      if (!monacoEditor) {{
                        return false;
                      }}
                      const nativeEditContext = monacoEditor.querySelector('.native-edit-context');
                      if (!nativeEditContext) {{
                        return false;
                      }}
                      const viewLine = monacoEditor.querySelector('.view-line');
                      if (!viewLine) {{
                        return false;
                      }}
                      monacoEditor.classList.add('focused');
                      editorContainer.classList.add('focused');
                      nativeEditContext.focus();
                      return true;
               }})();
               """
        return focus_js, target_selector