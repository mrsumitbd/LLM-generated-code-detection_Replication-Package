def create_dom_utility(agent_type: str) -> BaseDomUtils:
    if agent_type == 'browser':
        return BrowserDomUtils()
    elif agent_type == 'selenium':
        return SeleniumDomUtils()
    elif agent_type == 'appium':
        return AppiumDomUtils()
    else:
        raise ValueError("Unsupported utility type")