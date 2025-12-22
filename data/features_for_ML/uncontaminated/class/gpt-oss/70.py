from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple


def _human_readable_bytes(size: int, suffix: str = "B") -> str:
    """Convert a byte value into a human‑readable string."""
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei"):
        if abs(size) < 1024.0:
            return f"{size:3.1f}{unit}{suffix}"
        size /= 1024.0
    return f"{size:.1f}Yi{suffix}"


@dataclass(eq=True, frozen=True)
class StorageInfo:
    """Storage information structure.

    Attributes
    ----------
    total : int
        Total size of the filesystem in bytes.
    used : int
        Used space in bytes.
    free : int
        Free space in bytes.
    percent : float
        Percentage of used space (0.0–100.0).
    mountpoint : str
        Mount point of the filesystem.
    filesystem : str
        Filesystem type (e.g., ext4, ntfs).
    """

    total: int
    used: int
    free: int
    percent: float = field(init=False)
    mountpoint: str
    filesystem: str

    def __post_init__(self) -> None:
        # Compute percent if not provided
        object.__setattr__(self, "percent", round((self.used / self.total) * 100.0, 2))

    @classmethod
    def from_path(cls, path: str | Path) -> "StorageInfo":
        """Create a :class:`StorageInfo` instance from a filesystem path.

        Parameters
        ----------
        path : str | Path
            Path to a file or directory on the target filesystem.

        Returns
        -------
        StorageInfo
            Instance populated with statistics for the filesystem containing ``path``.
        """
        p = Path(path).expanduser().resolve()
        stat = os.statvfs(str(p))
        total = stat.f_frsize * stat.f_blocks
        free = stat.f_frsize * stat.f_bavail
        used = total - free
        # Attempt to get filesystem type via platform-specific calls
        filesystem = _guess_filesystem_type(p)
        return cls(total=total, used=used, free=free, mountpoint=str(p), filesystem=filesystem)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "StorageInfo":
        """Create a :class:`StorageInfo` instance from a mapping.

        Parameters
        ----------
        data : Mapping[str, Any]
            Mapping containing keys ``total``, ``used``, ``free``, ``mountpoint``, ``filesystem``.
            ``percent`` is optional and will be computed if missing.

        Returns
        -------
        StorageInfo
        """
        required = {"total", "used", "free", "mountpoint", "filesystem"}
        missing = required - data.keys()
        if missing:
            raise ValueError(f"Missing required keys: {missing}")
        return cls(
            total=int(data["total"]),
            used=int(data["used"]),
            free=int(data["free"]),
            mountpoint=str(data["mountpoint"]),
            filesystem=str(data["filesystem"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the instance."""
        return {
            "total": self.total,
            "used": self.used,
            "free": self.free,
            "percent": self.percent,
            "mountpoint": self.mountpoint,
            "filesystem": self.filesystem,
        }

    def __str__(self) -> str:
        return (
            f"StorageInfo(mountpoint={self.mountpoint!r}, filesystem={self.filesystem!r}, "
            f"total={_human_readable_bytes(self.total)}, used={_human_readable_bytes(self.used)}, "
            f"free={_human_readable_bytes(self.free)}, percent={self.percent:.2f}%)"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(total={self.total}, used={self.used}, free={self.free}, "
            f"mountpoint={self.mountpoint!r}, filesystem={self.filesystem!r})"
        )

    def update(self, path: str | Path) -> "StorageInfo":
        """Return a new :class:`StorageInfo` instance with updated statistics for the given path.

        Parameters
        ----------
        path : str | Path
            Path to a file or directory on the target filesystem.

        Returns
        -------
        StorageInfo
            New instance with refreshed statistics.
        """
        return self.from_path(path)

    @property
    def usage_ratio(self) -> float:
        """Return the ratio of used space to total space (0.0–1.0)."""
        return self.used / self.total if self.total else 0.0

    @property
    def free_ratio(self) -> float:
        """Return the ratio of free space to total space (0.0–1.0)."""
        return self.free / self.total if self.total else 0.0


def _guess_filesystem_type(path: Path) -> str:
    """Attempt to guess the filesystem type for a given path.

    This function uses platform‑specific mechanisms where available.
    """
    if sys.platform.startswith("win"):
        # On Windows, use ctypes to call GetVolumeInformationW
        try:
            import ctypes
            from ctypes import wintypes

            volume_name_buf = ctypes.create_unicode_buffer(1024)
            fs_name_buf = ctypes.create_unicode_buffer(1024)
            serial_number = wintypes.DWORD()
            max_component_len = wintypes.DWORD()
            file_system_flags = wintypes.DWORD()

            ret = ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(str(path)),
                volume_name_buf,
                ctypes.sizeof(volume_name_buf),
                ctypes.byref(serial_number),
                ctypes.byref(max_component_len),
                ctypes.byref(file_system_flags),
                fs_name_buf,
                ctypes.sizeof(fs_name_buf),
            )
            if ret:
                return fs_name_buf.value
        except Exception:
            pass
        return "unknown"
    else:
        # On POSIX, read /proc/mounts or use os.statvfs if available
        try:
            with open("/proc/mounts", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 3 and Path(parts[1]) == path:
                        return parts[2]
        except Exception:
            pass
        return "unknown"