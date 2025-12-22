def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    import ctypes
    import struct
    
    try:
        import dolphin
        dolphin.memory.write_u8(console_address, value & 0xFF)
    except (ImportError, AttributeError):
        try:
            import pyximport
            pyximport.install()
            from dolphin_memory import write_u8
            write_u8(console_address, value & 0xFF)
        except (ImportError, AttributeError):
            try:
                import subprocess
                import sys
                
                process = subprocess.Popen(
                    [sys.executable, "-c", 
                     f"import dolphin; dolphin.memory.write_u8({console_address}, {value & 0xFF})"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                process.wait()
            except Exception:
                pass