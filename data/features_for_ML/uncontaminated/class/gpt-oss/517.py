import logging
import random
from typing import Any, Dict, Optional

# Placeholder for the real SystemInitializer type
class SystemInitializer:
    """A minimal placeholder for the real SystemInitializer."""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

class CLIActivation:
    """
    CLI模式设备激活处理器.
    """

    def __init__(self, system_initializer: Optional[SystemInitializer] = None):
        """
        初始化 CLIActivation 实例。

        :param system_initializer: 可选的系统初始化器，用于获取配置信息。
        """
        self.system_initializer = system_initializer
        self.device_info: Dict[str, Any] = {}
        self.activation_result: Dict[str, Any] = {}
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)

    def _print_header(self):
        """
        打印激活流程的标题信息。
        """
        header = (
            "\n"
            "=========================================\n"
            "          设备激活流程开始\n"
            "=========================================\n"
        )
        self._log_and_print(header)

    def _update_device_info(self):
        """
        模拟更新设备信息。实际实现中应与硬件或服务交互。
        """
        # 这里仅做演示，生成一个随机设备 ID
        device_id = f"DEV-{random.randint(1000, 9999)}"
        self.device_info = {
            "device_id": device_id,
            "firmware_version": "1.0.3",
            "activation_status": "pending",
        }
        self._log_and_print(f"设备信息已更新: {self.device_info}")

    def _show_activation_info(self, activation_data: Dict[str, Any]):
        """
        显示激活所需的关键信息。

        :param activation_data: 激活数据字典。
        """
        info = (
            f"\n激活信息:\n"
            f"  设备 ID: {activation_data.get('device_id')}\n"
            f"  预期激活码: {activation_data.get('activation_code')}\n"
            f"  服务器地址: {activation_data.get('server_url')}\n"
        )
        self._log_and_print(info)

    def _print_activation_success(self):
        """
        打印激活成功信息。
        """
        success_msg = (
            "\n"
            "=========================================\n"
            "          设备激活成功\n"
            "=========================================\n"
        )
        self._log_and_print(success_msg)

    def _print_activation_failure(self):
        """
        打印激活失败信息。
        """
        failure_msg = (
            "\n"
            "=========================================\n"
            "          设备激活失败\n"
            "=========================================\n"
        )
        self._log_and_print(failure_msg)

    def _log_and_print(self, message: str):
        """
        同时记录日志并打印到终端。

        :param message: 要打印和记录的消息。
        """
        print(message)
        self.logger.info(message)

    def get_activation_result(self) -> Dict[str, Any]:
        """
        执行完整的激活流程并返回结果。

        :return: 包含激活结果的字典。
        """
        self._print_header()
        self._update_device_info()

        # 模拟激活数据
        activation_data = {
            "device_id": self.device_info["device_id"],
            "activation_code": "ABC123XYZ",
            "server_url": "https://activation.example.com/api",
        }
        self._show_activation_info(activation_data)

        # 随机决定激活是否成功
        success = random.choice([True, False])

        if success:
            self.device_info["activation_status"] = "activated"
            self._print_activation_success()
            self.activation_result = {
                "device_id": self.device_info["device_id"],
                "status": "success",
                "message": "Device activated successfully.",
            }
        else:
            self.device_info["activation_status"] = "failed"
            self._print_activation_failure()
            self.activation_result = {
                "device_id": self.device_info["device_id"],
                "status": "failure",
                "message": "Device activation failed.",
            }

        return self.activation_result