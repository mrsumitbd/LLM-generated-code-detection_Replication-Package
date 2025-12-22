import shutil
from pathlib import Path

def _detect_boot() -> Boot:
    if shutil.which("grubby"):
        return Boot.GRUBBY
    if Path("/boot/loader/entries").exists():
        return Boot.SYSTEMD_BOOT
    if Path("/boot/grub2/grub.cfg").exists():
        return Boot.GRUB2_MODERN
    if Path("/boot/grub/grub.cfg").exists():
        return Boot.GRUB2_LEGACY
    return Boot.UNKNOWN