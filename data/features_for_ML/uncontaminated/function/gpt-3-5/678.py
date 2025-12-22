def rules_dir_writable() -> bool:
    import os
    return os.access('/etc/prometheus/rules', os.W_OK)