def get_arch(system: PLATFORM) -> str:
    import platform
    
    machine = platform.machine().lower()
    
    if machine in ('x86_64', 'amd64'):
        return 'x86_64'
    elif machine in ('i386', 'i686', 'x86'):
        return 'x86'
    elif machine in ('aarch64', 'arm64'):
        return 'aarch64'
    elif machine in ('armv7l', 'armv7'):
        return 'armv7'
    elif machine in ('armv6l',):
        return 'armv6'
    elif machine in ('ppc64le',):
        return 'ppc64le'
    elif machine in ('ppc64',):
        return 'ppc64'
    elif machine in ('s390x',):
        return 's390x'
    elif machine in ('riscv64',):
        return 'riscv64'
    else:
        return machine