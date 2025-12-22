def get_pip_sys_values() -> SysValues:
    """
    Returns various sys values as they are in the *target* environment.
    This is because pipask is typically installed in a different environment (e.g., pipx)
    than the installation target environment.
    """
    import sys
    import sysconfig
    
    return SysValues(
        prefix=sysconfig.get_path("data"),
        exec_prefix=sysconfig.get_path("platlib"),
        base_prefix=sys.base_prefix,
        base_exec_prefix=sys.base_exec_prefix,
        platlib=sysconfig.get_path("platlib"),
        purelib=sysconfig.get_path("purelib"),
        include=sysconfig.get_path("include"),
        scripts=sysconfig.get_path("scripts"),
        stdlib=sysconfig.get_path("stdlib"),
        platstdlib=sysconfig.get_path("platstdlib"),
    )