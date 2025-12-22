def analyze_program(
    self,
    df_or_prog: Union["DomainFile", "Program"],
    require_symbols: bool = True,
    force_analysis: bool = False,
    verbose_analysis: bool = False,
):
    if isinstance(df_or_prog, DomainFile):
        program = df_or_prog.program
    else:
        program = df_or_prog

    if force_analysis or program.needs_analysis():
        program.analyze(
            require_symbols=require_symbols,
            verbose=verbose_analysis,
        )

    return program