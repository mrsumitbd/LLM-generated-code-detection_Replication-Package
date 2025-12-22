class CLIActivation:
    """
    CLI模式设备激活处理器.
    """

    def __init__(self, system_initializer: Optional[SystemInitializer] = None):
        self.system_initializer = system_initializer
        self.activation_result = {
            "success": False,
            "message": "",
            "device_info": {},
            "activation_data": {}
        }
        self.logger = logging.getLogger(__name__)

    def _print_header(self):
        print("=" * 60)
        print("设备激活处理器 - CLI模式")
        print("=" * 60)
        print()

    def _update_device_info(self):
        try:
            if self.system_initializer:
                device_info = self.system_initializer.get_device_info()
                self.activation_result["device_info"] = device_info
                self._log_and_print(f"设备信息已更新: {device_info}")
            else:
                self._log_and_print("警告: 系统初始化器未配置")
        except Exception as e:
            self._log_and_print(f"更新设备信息失败: {str(e)}")
            self.logger.error(f"Error updating device info: {e}")

    def _show_activation_info(self, activation_data: dict):
        print("\n激活信息:")
        print("-" * 60)
        for key, value in activation_data.items():
            print(f"  {key}: {value}")
        print("-" * 60)
        print()
        self.activation_result["activation_data"] = activation_data

    def _print_activation_success(self):
        print("\n" + "=" * 60)
        print("✓ 设备激活成功!")
        print("=" * 60)
        print()
        self.activation_result["success"] = True
        self.activation_result["message"] = "设备激活成功"
        self.logger.info("Device activation successful")

    def _print_activation_failure(self):
        print("\n" + "=" * 60)
        print("✗ 设备激活失败!")
        print("=" * 60)
        print()
        self.activation_result["success"] = False
        self.activation_result["message"] = "设备激活失败"
        self.logger.error("Device activation failed")

    def _log_and_print(self, message: str):
        print(message)
        self.logger.info(message)

    def get_activation_result(self) -> dict:
        return self.activation_result