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
    agent_type = agent_type.lower().strip()
    
    if agent_type == 'browser':
        from browser_dom_utils import BrowserDomUtils
        return BrowserDomUtils()
    elif agent_type == 'selenium':
        from selenium_dom_utils import SeleniumDomUtils
        return SeleniumDomUtils()
    elif agent_type == 'appium':
        from appium_dom_utils import AppiumDomUtils
        return AppiumDomUtils()
    else:
        raise ValueError(f"Unsupported DOM utility type: '{agent_type}'. "
                        f"Must be one of 'browser', 'selenium', or 'appium'.")