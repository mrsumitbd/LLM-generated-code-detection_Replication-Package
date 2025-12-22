from typing import Final, Mapping, Type
from SelfhealingAgents.self_healing_system.context_retrieving.library_dom_utils.base_dom_utils import BaseDomUtils

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
        dom_utility: Type[BaseDomUtils] = _DOM_UTILITY_TYPE.get(agent_type)
        if dom_utility is None:
            raise ValueError(f"Unsupported DOM utility type: {dom_utility}")
        return dom_utility()