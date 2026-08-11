"""统一管理测试环境中的设备对象。"""

from pathlib import Path

from config import load_device_config
from ssh_device import SSHDevice


class DeviceManager:
    """统一创建、缓存和释放测试设备。"""

    def __init__(
        self,
        config_path: str | Path,
    ) -> None:
        self._config_path = Path(config_path)

        # 已经创建并连接的设备
        self._devices: dict[str, SSHDevice] = {}

    def get(self, name: str) -> SSHDevice:
        """根据设备名称获取设备对象。"""

        # 已经创建过，直接复用
        if name in self._devices:
            return self._devices[name]

        # 使用现有 config.py 读取指定设备
        connection_params = load_device_config(
            self._config_path,
            name,
        )

        device = SSHDevice(
            name=name,
            connection_params=connection_params,
        )

        device.connect()

        # 缓存设备对象
        self._devices[name] = device

        return device

    def disconnect_all(self) -> None:
        """断开所有已经创建的设备连接。"""

        for device in self._devices.values():
            device.disconnect()

        self._devices.clear()