from __future__ import annotations

import sys
import platform
from typing import Any, Dict

def _get_importlib_metadata() -> Any:
    """Return importlib.metadata module or None if unavailable."""
    try:
        import importlib.metadata as metadata  # type: ignore
        return metadata
    except Exception:
        return None

def _get_pkg_resources() -> Any:
    """Return pkg_resources module or None if unavailable."""
    try:
        import pkg_resources  # type: ignore
        return pkg_resources
    except Exception:
        return None

def _get_installed_packages() -> Dict[str, str]:
    """Return a mapping of installed package names to their versions."""
    metadata = _get_importlib_metadata()
    if metadata is not None:
        try:
            return {dist.metadata["Name"]: dist.version for dist in metadata.distributions()}
        except Exception:
            pass

    pkg_resources = _get_pkg_resources()
    if pkg_resources is not None:
        try:
            return {dist.project_name: dist.version for dist in pkg_resources.working_set}
        except Exception:
            pass

    # Fallback: empty dict
    return {}

def _get_pip_version() -> str | None:
    """Return the pip version if available."""
    metadata = _get_importlib_metadata()
    if metadata is not None:
        try:
            return metadata.version("pip")
        except Exception:
            pass

    pkg_resources = _get_pkg_resources()
    if pkg_resources is not None:
        try:
            return pkg_resources.get_distribution("pip").version
        except Exception:
            pass

    return None

def get_installation_info() -> Dict[str, Dict[str, Any]]:
    """
    Gather information about the current Python installation.

    Returns:
        A dictionary with the following structure:
        {
            "python": {
                "implementation": str,
                "version": str,
                "executable": str,
            },
            "platform": {
                "system": str,
                "release": str,
                "version": str,
                "machine": str,
            },
            "pip": {
                "version": str | None,
            },
            "packages": {
                <package_name>: <package_version>,
                ...
            }
        }
    """
    python_info: Dict[str, Any] = {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "executable": sys.executable,
    }

    platform_info: Dict[str, Any] = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
    }

    pip_info: Dict[str, Any] = {
        "version": _get_pip_version(),
    }

    packages_info: Dict[str, str] = _get_installed_packages()

    return {
        "python": python_info,
        "platform": platform_info,
        "pip": pip_info,
        "packages": packages_info,
    }