from collections.abc import Mapping
from ruamel.yaml import YAML

def get_options(options_or_path):
            if isinstance(options_or_path, Mapping):
                return options_or_path
            elif isinstance(options_or_path, str):
                yaml = YAML()  # automatically supports json :)
                with open(options_or_path, "r") as f:
                    options = yaml.load(f)
                return options