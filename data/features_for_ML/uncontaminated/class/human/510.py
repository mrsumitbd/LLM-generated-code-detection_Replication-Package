from dataclasses import dataclass, field
from typing import List, Literal, Optional

class ChromeConfig:
    """Configuration for Chrome driver."""

    headless: bool = True
    chromedriver_path: Optional[str] = None
    browser_args: List[str] = field(default_factory=list)
    user_agent: Optional[str] = None