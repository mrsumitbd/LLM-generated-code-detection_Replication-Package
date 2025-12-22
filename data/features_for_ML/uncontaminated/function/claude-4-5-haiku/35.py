def _log_debug_end(translator: Translator, variables: GraphVariables) -> None:
    if translator.debug:
        print(f"[DEBUG END] Graph translation completed")
        print(f"[DEBUG END] Total variables: {len(variables.variables)}")
        for var_name, var_info in variables.variables.items():
            print(f"[DEBUG END]   - {var_name}: {var_info}")