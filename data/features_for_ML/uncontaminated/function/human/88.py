import sys
from importlib.util import find_spec

def module_checker(class_name: str) -> None:
        """
        Checks if required config plugins are present before running the ARES pipeline.

        This function verifies the presence of a specified plugin before proceeding with the ARES pipeline execution.

        :param class_name: The name of the plugin to check for.
        """
        logger.info("Checking for presence of: %s", class_name)
        try:
            # Looking for an absolute class path - not tool native - external
            ret = find_spec(class_name)
            if ret is None:
                raise ModuleNotFoundError()
        except ModuleNotFoundError as no_mod:
            # Looking for a specific class
            package = class_name.rsplit(".", 1)
            if len(package) != 2:
                raise no_mod
            try:
                output = find_spec(package[0])
                if output is None:
                    raise no_mod
            except ModuleNotFoundError:
                plugin_name = package[0]
                plugin_name = plugin_name.split(".")[0].replace("_", "-")

                logger.error("Following plugin not found: %s", plugin_name)
                logger.error("Install with: ares install-plugin %s", plugin_name)
                sys.exit()