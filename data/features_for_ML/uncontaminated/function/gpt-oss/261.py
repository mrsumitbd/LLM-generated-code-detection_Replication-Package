import sys
import json
import logging
from pathlib import Path

# Optional: use requests if available, otherwise fallback to urllib
try:
    import requests
except ImportError:
    requests = None
    import urllib.request as urllib_request
    import urllib.error as urllib_error

# Optional: use packaging.version for robust comparison
try:
    from packaging.version import Version, InvalidVersion
except ImportError:
    Version = None
    InvalidVersion = Exception

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Configuration – adjust these constants to match your package
# --------------------------------------------------------------------------- #
PACKAGE_NAME = "my_package"          # Replace with your actual package name
CURRENT_VERSION = "0.0.0"           # Replace with your current version string
UPDATE_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _fetch_latest_version(url: str) -> str | None:
    """
    Fetch the latest version string from the given JSON URL.
    Returns None if the request fails or the JSON is malformed.
    """
    try:
        if requests:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
        else:
            with urllib_request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        logger.debug("Failed to fetch update info: %s", exc)
        return None

    try:
        return data["info"]["version"]
    except (KeyError, TypeError):
        logger.debug("Malformed JSON response: %s", data)
        return None


def _parse_version(vstr: str) -> Version | None:
    """
    Parse a version string into a packaging.version.Version object.
    Returns None if parsing fails.
    """
    if Version is None:
        # Fallback: simple tuple comparison
        try:
            return tuple(int(part) for part in vstr.split("."))
        except Exception:
            return None
    try:
        return Version(vstr)
    except InvalidVersion:
        return None


def _is_newer(latest: Version | tuple, current: Version | tuple) -> bool:
    """
    Return True if 'latest' is newer than 'current'.
    """
    if latest is None or current is None:
        return False
    return latest > current


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def check_and_notify() -> None:
    """
    Check for updates and notify user if available.

    This is the main entry point for version checking.
    """
    # Resolve current version
    current_ver = _parse_version(CURRENT_VERSION)
    if current_ver is None:
        logger.warning("Could not parse current version '%s'. Skipping update check.", CURRENT_VERSION)
        return

    # Fetch latest version
    latest_str = _fetch_latest_version(UPDATE_URL)
    if not latest_str:
        logger.debug("Could not retrieve latest version info.")
        return

    latest_ver = _parse_version(latest_str)
    if latest_ver is None:
        logger.warning("Could not parse latest version '%s'.", latest_str)
        return

    # Compare and notify
    if _is_newer(latest_ver, current_ver):
        logger.info(
            "A new version of %s is available: %s (you have %s). "
            "Please consider updating.",
            PACKAGE_NAME,
            latest_str,
            CURRENT_VERSION,
        )
    else:
        logger.debug("You are running the latest version (%s).", CURRENT_VERSION)


# --------------------------------------------------------------------------- #
# If this module is executed directly, run the check
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    check_and_notify()