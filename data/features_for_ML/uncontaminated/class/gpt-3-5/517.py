from typing import Optional

class CLIActivation:
    """
    CLI模式设备激活处理器.
    """

    def __init__(self, system_initializer: Optional[SystemInitializer] = None):
        self.system_initializer = system_initializer
        self.activation_result = {}

    def _print_header(self):
        print("Activating device in CLI mode...")

    def _update_device_info(self):
        # Update device info logic here
        pass

    def _show_activation_info(self, activation_data: dict):
        print("Activation Info:")
        for key, value in activation_data.items():
            print(f"{key}: {value}")

    def _print_activation_success(self):
        print("Device activation successful.")

    def _print_activation_failure(self):
        print("Device activation failed.")

    def _log_and_print(self, message: str):
        print(message)

    def get_activation_result(self) -> dict:
        return self.activation_result