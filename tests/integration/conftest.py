"""真实设备集成测试使用的 fixtures。"""

import os
from getpass import getpass
from pathlib import Path

import pytest

from topology import load_topology
from config import load_device_config
from device_manager import DeviceManager

from cleanup import CleanupManager

PROJECT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_DIR / "devices.yaml"
TOPOLOGY_CONFIG_PATH = (
    PROJECT_DIR / "topology.yaml"
)

@pytest.fixture(scope="session")
def device_manager():
    """整个 pytest session 共用一个设备管理器。"""

    

    manager = DeviceManager(
        config_path=CONFIG_PATH
    )

    yield manager

    manager.disconnect_all()

@pytest.fixture(scope="session")
def topology():
    """提供当前测试拓扑信息。"""

    return load_topology(
        TOPOLOGY_CONFIG_PATH
    )

@pytest.fixture
def real_r1(device_manager):
    """返回 R1 设备对象。"""
    return device_manager.get("r1")

@pytest.fixture
def real_r2(device_manager):
    """返回 R2 设备对象。"""
    return device_manager.get("r2")

@pytest.fixture
def cleanup_manager():
    """为单条测试提供环境恢复能力。"""

    manager = CleanupManager()

    yield manager

    manager.run()



# @pytest.fixture
# def temporary_loopback(
#     real_r1: SSHDevice,
# ):
#     """创建临时 Loopback，测试结束后自动删除。"""

#     loopback_info = {
#         "name": "Loopback99",
#         "ip": "10.255.99.1",
#         "mask": "255.255.255.255",
#     }

#     real_r1.execute_config(
#         commands=[
#             f"interface {loopback_info['name']}",
#             "description NETLAB_PYTEST_TEMP",
#             (
#                 f"ip address "
#                 f"{loopback_info['ip']} "
#                 f"{loopback_info['mask']}"
#             ),
#             "no shutdown",
#         ],
#         read_timeout=30,
#     )

#     try:
#         yield loopback_info

#     finally:
#         real_r1.execute_config(
#             commands=[
#                 f"no interface {loopback_info['name']}",
#             ],
#             read_timeout=30,
#         )