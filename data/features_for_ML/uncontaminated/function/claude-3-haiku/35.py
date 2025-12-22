def _log_debug_end(translator: Translator, variables: GraphVariables) -> None:
    logger = translator.get_logger()
    logger.debug(f"End of graph execution. Variables: {variables}")