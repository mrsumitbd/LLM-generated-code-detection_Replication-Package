import json
import anthropic


class Config:

    def to_json(self):
        """Convert the Config object to a JSON string."""
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str):
        """Create a Config object from a JSON string."""
        config_dict = json.loads(data)
        config = Config()
        for key, value in config_dict.items():
            setattr(config, key, value)
        return config


def main():
    # Test the Config class
    config = Config()
    config.model = "claude-3-5-sonnet-20241022"
    config.max_tokens = 1024
    config.temperature = 0.7

    # Test to_json
    json_str = config.to_json()
    print("JSON representation:")
    print(json_str)

    # Test from_json
    config2 = Config.from_json(json_str)
    print("\nRestored config:")
    print(f"model: {config2.model}")
    print(f"max_tokens: {config2.max_tokens}")
    print(f"temperature: {config2.temperature}")

    # Verify they match
    assert config.model == config2.model
    assert config.max_tokens == config2.max_tokens
    assert config.temperature == config2.temperature
    print("\nAll tests passed!")


if __name__ == "__main__":
    main()