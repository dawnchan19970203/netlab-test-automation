"""负责读取和检查设备 YAML 配置。"""

from pathlib import Path
from typing import Any

import yaml


REQUIRED_DEVICE_FIELDS = (
    "device_type",
    "host",
    "username",
    "password"
)


def load_device_config(
    config_path: str | Path,
    device_name: str,
) -> dict[str, Any]:
    """
    从 YAML 文件中读取一台设备的配置。

    参数：
        config_path: YAML 配置文件路径
        device_name: devices 字段下的设备名称，例如 r1

    返回：
        Netmiko 可以使用的设备参数字典

    异常：
        FileNotFoundError: 配置文件不存在
        ValueError: YAML 内容或设备配置不正确
    """

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"设备配置文件不存在：{path}"
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            raw_config = yaml.safe_load(file)

    except yaml.YAMLError as exc:
        raise ValueError(
            f"YAML 格式错误：{exc}"
        ) from exc

    if not isinstance(raw_config, dict):
        raise ValueError(
            "YAML 顶层必须是一个字典。"
        )

    devices = raw_config.get("devices")

    if not isinstance(devices, dict) or not devices:
        raise ValueError(
            "YAML 必须包含非空的 devices 字段。"
        )

    raw_device = devices.get(device_name)

    if not isinstance(raw_device, dict):
        available_devices = ", ".join(
            sorted(devices.keys())
        )

        raise ValueError(
            f"没有找到设备 {device_name!r}。"
            f"当前可用设备：{available_devices}"
        )

    missing_fields = [
        field_name
        for field_name in REQUIRED_DEVICE_FIELDS
        if not raw_device.get(field_name)
    ]

    if missing_fields:
        raise ValueError(
            f"设备 {device_name!r} 缺少必要字段："
            f"{', '.join(missing_fields)}"
        )

    # 创建新字典，避免后续添加密码时修改原始 YAML 数据
    device_info = dict(raw_device)

    # 未配置端口时，默认使用 SSH 端口 22
    device_info.setdefault("port", 22)

    port = device_info["port"]

    if (
        isinstance(port, bool)
        or not isinstance(port, int)
        or not 1 <= port <= 65535
    ):
        raise ValueError(
            f"设备 {device_name!r} 的 port "
            "必须是 1～65535 之间的整数。"
        )

    return device_info