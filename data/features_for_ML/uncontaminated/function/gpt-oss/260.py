from typing import Union

def analyze_program(  # noqa C901
        self,
        df_or_prog: Union["DomainFile", "Program"],
        require_symbols: bool = True,
        force_analysis: bool = False,
        verbose_analysis: bool = False,
    ):
    """
    Analyze a :class:`DomainFile` or :class:`Program`.

    Parameters
    ----------
    df_or_prog : Union[DomainFile, Program]
        The object to analyze.  If a :class:`DomainFile` is supplied,
        it will be converted to a :class:`Program` using its ``to_program``
        method (if available).  If a :class:`Program` is supplied it will
        be used directly.
    require_symbols : bool, default True
        If ``True`` the program must expose a ``symbols`` attribute after
        analysis.  If the attribute is missing a :class:`RuntimeError`
        is raised.
    force_analysis : bool, default False
        If ``True`` the analysis will be performed even if the program
        already reports that it has been analysed.
    verbose_analysis : bool, default False
        If ``True`` a short message is printed to ``stdout`` before
        performing the analysis.

    Returns
    -------
    Program
        The analysed program instance.
    """
    # ------------------------------------------------------------------
    # Resolve the program object
    # ------------------------------------------------------------------
    # If the caller passed a DomainFile, try to convert it to a Program.
    if hasattr(df_or_prog, "to_program"):
        prog = df_or_prog.to_program()
    else:
        prog = df_or_prog

    # ------------------------------------------------------------------
    # Perform analysis if required
    # ------------------------------------------------------------------
    # Determine whether the program has already been analysed.
    already_analyzed = getattr(prog, "_analysis_done", False)

    if force_analysis or not already_analyzed:
        if verbose_analysis:
            try:
                name = getattr(prog, "name", repr(prog))
            except Exception:
                name = repr(prog)
            print(f"[analyze_program] Analyzing program: {name}")

        # The program is expected to provide an ``analyze`` method.
        if not hasattr(prog, "analyze"):
            raise AttributeError(
                f"Object of type {type(prog).__name__} does not provide an 'analyze' method."
            )

        # Call the program's analysis routine.
        prog.analyze(require_symbols=require_symbols)

        # Mark the program as analysed.
        setattr(prog, "_analysis_done", True)

    else:
        if verbose_analysis:
            try:
                name = getattr(prog, "name", repr(prog))
            except Exception:
                name = repr(prog)
            print(f"[analyze_program] Skipping analysis for program: {name}")

    # ------------------------------------------------------------------
    # Verify that symbols are present if required
    # ------------------------------------------------------------------
    if require_symbols and not hasattr(prog, "symbols"):
        raise RuntimeError(
            f"Program {prog!r} does not expose a 'symbols' attribute after analysis."
        )

    return prog