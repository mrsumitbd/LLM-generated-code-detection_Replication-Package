from __future__ import annotations

from typing import Any, Dict, Sequence

# Import the pip InstallRequirement type if available
try:
    from pip._internal.req import InstallRequirement
except Exception:  # pragma: no cover
    # Fallback for environments where pip is not importable
    InstallRequirement = Any


class InstallationReport:
    """
    A lightweight wrapper around a sequence of :class:`pip._internal.req.InstallRequirement`
    objects that can be serialised to a plain dictionary.
    """

    def __init__(self, install_requirements: Sequence[InstallRequirement]):
        """
        Store the given sequence of :class:`InstallRequirement` objects.

        Parameters
        ----------
        install_requirements
            A sequence of :class:`InstallRequirement` instances.
        """
        self._install_requirements = list(install_requirements)

    @classmethod
    def _install_req_to_dict(cls, ireq: InstallRequirement) -> Dict[str, Any]:
        """
        Convert a single :class:`InstallRequirement` into a dictionary.

        The dictionary contains a subset of the most useful attributes of the
        requirement.  Missing attributes are omitted.

        Parameters
        ----------
        ireq
            The :class:`InstallRequirement` instance to serialise.

        Returns
        -------
        dict
            A dictionary representation of the requirement.
        """
        data: Dict[str, Any] = {}

        # Basic identification
        data["name"] = getattr(ireq, "name", None)

        # Requirement specifier (e.g. ">=1.0,<2.0")
        req = getattr(ireq, "req", None)
        if req is not None:
            data["specifier"] = str(req.specifier) if req.specifier else None
            data["extras"] = list(req.extras) if req.extras else None
            data["markers"] = str(req.marker) if req.marker else None
            data["requires_python"] = req.requires_python
            data["requires_dist"] = list(req.requires_dist) if req.requires_dist else None

        # Location information
        data["location"] = getattr(ireq, "location", None)
        data["installed_location"] = getattr(ireq, "installed_location", None)

        # Link / URL information
        link = getattr(ireq, "link", None)
        if link is not None:
            data["link"] = str(link)
        data["url"] = getattr(ireq, "url", None)

        # Flags
        for flag in (
            "editable",
            "is_direct",
            "is_wheel",
            "is_sdist",
            "is_file",
            "is_url",
            "is_local",
        ):
            value = getattr(ireq, flag, None)
            if value is not None:
                data[flag] = value

        # Hashes and direct URL
        hashes = getattr(ireq, "hashes", None)
        if hashes:
            data["hashes"] = [str(h) for h in hashes]
        direct_url = getattr(ireq, "direct_url", None)
        if direct_url:
            data["direct_url"] = direct_url

        # Remove keys with None values
        return {k: v for k, v in data.items() if v is not None}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialise the entire report to a dictionary.

        Returns
        -------
        dict
            A dictionary containing a list of serialised requirements.
        """
        return {
            "install_requirements": [
                self._install_req_to_dict(ireq) for ireq in self._install_requirements
            ]
        }