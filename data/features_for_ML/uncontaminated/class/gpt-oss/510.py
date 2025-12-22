from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

try:
    from selenium.webdriver import Chrome, ChromeOptions
    from selenium.webdriver.chrome.service import Service
except ImportError as exc:
    raise ImportError(
        "Selenium is required to use ChromeConfig. "
        "Install it with `pip install selenium`."
    ) from exc


@dataclass
class ChromeConfig:
    """Configuration for Chrome driver."""

    headless: bool = False
    window_size: Optional[Tuple[int, int]] = None
    binary_location: Optional[str] = None
    user_data_dir: Optional[str] = None
    args: List[str] = field(default_factory=list)
    extensions: List[str] = field(default_factory=list)
    proxy: Optional[str] = None
    capabilities: Dict[str, object] = field(default_factory=dict)
    service_args: List[str] = field(default_factory=list)
    service_log_path: Optional[str] = None
    driver_path: Optional[str] = None

    def __post_init__(self) -> None:
        # Normalise args and extensions to lists
        self.args = list(self.args)
        self.extensions = list(self.extensions)
        self.service_args = list(self.service_args)

    # ------------------------------------------------------------------
    #  Configuration helpers
    # ------------------------------------------------------------------
    def set_headless(self, headless: bool = True) -> None:
        self.headless = headless

    def set_window_size(self, width: int, height: int) -> None:
        self.window_size = (width, height)

    def set_binary_location(self, path: str) -> None:
        self.binary_location = path

    def set_user_data_dir(self, path: str) -> None:
        self.user_data_dir = path

    def add_argument(self, arg: str) -> None:
        self.args.append(arg)

    def add_extension(self, path: str) -> None:
        self.extensions.append(path)

    def set_proxy(self, proxy: str) -> None:
        self.proxy = proxy

    def set_capabilities(self, caps: Dict[str, object]) -> None:
        self.capabilities = caps

    def add_service_arg(self, arg: str) -> None:
        self.service_args.append(arg)

    def set_service_log_path(self, path: str) -> None:
        self.service_log_path = path

    def set_driver_path(self, path: str) -> None:
        self.driver_path = path

    # ------------------------------------------------------------------
    #  Conversion helpers
    # ------------------------------------------------------------------
    def to_options(self) -> ChromeOptions:
        """Return a ChromeOptions instance configured from this object."""
        options = ChromeOptions()

        if self.headless:
            options.add_argument("--headless")
        if self.window_size:
            options.add_argument(f"--window-size={self.window_size[0]},{self.window_size[1]}")
        if self.binary_location:
            options.binary_location = self.binary_location
        if self.user_data_dir:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
        for arg in self.args:
            options.add_argument(arg)
        for ext in self.extensions:
            options.add_extension(ext)
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")

        return options

    def to_service(self) -> Service:
        """Return a Service instance configured from this object."""
        service = Service(executable_path=self.driver_path or "")
        if self.service_args:
            service.service_args = self.service_args
        if self.service_log_path:
            service.log_path = self.service_log_path
        return service

    # ------------------------------------------------------------------
    #  Driver creation
    # ------------------------------------------------------------------
    def get_driver(self) -> Chrome:
        """Instantiate and return a Selenium Chrome driver."""
        options = self.to_options()
        service = self.to_service()
        driver = Chrome(service=service, options=options, desired_capabilities=self.capabilities)
        return driver

    # ------------------------------------------------------------------
    #  Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, object]:
        """Return a dictionary representation of the configuration."""
        return {
            "headless": self.headless,
            "window_size": self.window_size,
            "binary_location": self.binary_location,
            "user_data_dir": self.user_data_dir,
            "args": list(self.args),
            "extensions": list(self.extensions),
            "proxy": self.proxy,
            "capabilities": dict(self.capabilities),
            "service_args": list(self.service_args),
            "service_log_path": self.service_log_path,
            "driver_path": self.driver_path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "ChromeConfig":
        """Create a ChromeConfig instance from a dictionary."""
        return cls(
            headless=data.get("headless", False),
            window_size=tuple(data["window_size"]) if data.get("window_size") else None,
            binary_location=data.get("binary_location"),
            user_data_dir=data.get("user_data_dir"),
            args=data.get("args", []),
            extensions=data.get("extensions", []),
            proxy=data.get("proxy"),
            capabilities=data.get("capabilities", {}),
            service_args=data.get("service_args", []),
            service_log_path=data.get("service_log_path"),
            driver_path=data.get("driver_path"),
        )

    # ------------------------------------------------------------------
    #  Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        attrs = [
            f"headless={self.headless}",
            f"window_size={self.window_size}",
            f"binary_location={self.binary_location!r}",
            f"user_data_dir={self.user_data_dir!r}",
            f"args={self.args!r}",
            f"extensions={self.extensions!r}",
            f"proxy={self.proxy!r}",
            f"capabilities={self.capabilities!r}",
            f"service_args={self.service_args!r}",
            f"service_log_path={self.service_log_path!r}",
            f"driver_path={self.driver_path!r}",
        ]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __iter__(self) -> Iterable[tuple[str, object]]:
        """Iterate over configuration items."""
        yield from self.to_dict().items()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChromeConfig):
            return NotImplemented
        return self.to_dict() == other.to_dict()