def _detect_boot() -> Boot:
    import os
    if os.path.exists('/boot/uboot/uboot.env'):
        return Boot.UBOOT
    elif os.path.exists('/boot/grub/grub.cfg'):
        return Boot.GRUB
    else:
        return Boot.UNKNOWN