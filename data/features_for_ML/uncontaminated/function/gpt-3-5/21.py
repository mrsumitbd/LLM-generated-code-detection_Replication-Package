def write_byte(console_address: int, value: int) -> None:
    import struct
    from ctypes import windll, c_int, c_void_p

    kernel32 = windll.kernel32
    process_all_access = 0x1F0FFF
    process_handle = kernel32.OpenProcess(process_all_access, False, 0x1C04)  # 0x1C04 is the process ID of Dolphin emulator

    if process_handle:
        buffer = struct.pack('B', value)
        buffer_size = len(buffer)
        bytes_written = c_int(0)
        kernel32.WriteProcessMemory(process_handle, console_address, buffer, buffer_size, c_void_p(bytes_written))

        kernel32.CloseHandle(process_handle)