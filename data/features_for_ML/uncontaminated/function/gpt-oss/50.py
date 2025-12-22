from .base_dom_utils import BaseDomUtils
from .browser_dom_utils import BrowserDomUtils
from .selenium_dom_utils import SeleniumDomUtils
from .appium_dom_utils import AppiumDomUtils

def create_dom_utility(agent_type: str) -> BaseDomUtils:
    """Creates a DOM utility instance based on the specified type.

    Args:
        agent_type (str): The type of DOM utility to create. Should be one of
            'browser', 'selenium', or 'appium'.

    Returns:
        BaseDomUtils: An instance of the appropriate DOM utility class.

    Raises:
        ValueError: If the utility type is not supported.
    """
    if agent_type == "browser":
        return BrowserDomUtils()
    if agent_type == "selenium":
        return SeleniumDomUtils()
    if agent_type == "appium":
        return AppiumDomUtils()
    raise ValueError(f"Unsupported DOM utility type: {agent_type}")