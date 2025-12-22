from typing import Optional

class SystemInitializer:
    pass

class CLIActivation:
    """
    CLI模式设备激活处理器.
    """

    def __init__(self, system_initializer: Optional[SystemInitializer] = None):
        self._system_initializer = system_initializer
        self._activation_data = {}

    def _print_header(self):
        print("Device Activation")
        print("----------------")

    def _update_device_info(self):
        device_info = self._system_initializer.get_device_info()
        self._activation_data["device_info"] = device_info

    def _show_activation_info(self, activation_data: dict):
        print(f"Device ID: {activation_data['device_info']['device_id']}")
        print(f"Activation Code: {activation_data['activation_code']}")

    def _print_activation_success(self):
        print("Activation successful!")

    def _print_activation_failure(self):
        print("Activation failed.")

    def _log_and_print(self, message: str):
        print(message)
        # Log the message to a file or database

    def get_activation_result(self) -> dict:
        self._print_header()
        self._update_device_info()
        activation_code = self._system_initializer.generate_activation_code()
        self._activation_data["activation_code"] = activation_code
        self._show_activation_info(self._activation_data)

        if self._system_initializer.activate_device(activation_code):
            self._print_activation_success()
        else:
            self._print_activation_failure()

        return self._activation_data