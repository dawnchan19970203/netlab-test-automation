"""测试 SSHDevice 的基础状态和参数检查。"""

import pytest

from exceptions import (
    CommandExecutionError,
    DeviceAuthenticationError,
    DeviceConnectionError,
    DeviceStateError,
)
from ssh_device import SSHDevice

from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)
import ssh_device as ssh_device_module



@pytest.fixture
def unconnected_device() -> SSHDevice:
    """提供一个尚未建立 SSH 连接的设备对象。"""

    return SSHDevice(
        name="r1",
        connection_params={},
    )


def test_new_device_is_not_connected(
    unconnected_device: SSHDevice,
) -> None:
    """新创建的设备对象应该处于未连接状态。"""

    assert unconnected_device.is_connected is False


def test_empty_command_raises_error(
    unconnected_device: SSHDevice,
) -> None:
    """空命令应该抛出 CommandExecutionError。"""

    with pytest.raises(
        CommandExecutionError,
        match="设备命令不能为空",
    ):
        unconnected_device.execute_command("   ")


def test_command_without_connection_raises_error(
    unconnected_device: SSHDevice,
) -> None:
    """未连接时执行正常命令，应该抛出 DeviceStateError。"""

    with pytest.raises(
        DeviceStateError,
        match="尚未建立 SSH 连接",
    ):
        unconnected_device.execute_command(
            "show version"
        )

def test_connect_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """模拟 SSH 连接成功。"""

    fake_connection = FakeConnection()

    def fake_connect_handler(**connection_params):
        return fake_connection

    monkeypatch.setattr(
        ssh_device_module,
        "ConnectHandler",
        fake_connect_handler,
    )

    device = SSHDevice(
        name="r1",
        connection_params={
            "host": "172.16.100.11",
            "username": "netlab",
            "password": "fake-password",
            "device_type": "cisco_ios",
        },
    )

    assert device.is_connected is False

    device.connect()

    assert device.is_connected is True

    device.disconnect()

    assert device.is_connected is False
    assert fake_connection.disconnected is True


def test_connect_timeout_raises_device_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """底层连接超时应该转换成项目连接异常。"""

    def fake_connect_handler(**connection_params):
        raise NetmikoTimeoutException(
            "模拟 SSH 连接超时"
        )

    monkeypatch.setattr(
        ssh_device_module,
        "ConnectHandler",
        fake_connect_handler,
    )

    device = SSHDevice(
        name="r1",
        connection_params={
            "host": "172.16.100.11",
            "username": "netlab",
            "password": "fake-password",
            "device_type": "cisco_ios",
        },
    )

    with pytest.raises(
        DeviceConnectionError,
        match="连接设备 'r1' 超时",
    ):
        device.connect()

    assert device.is_connected is False

def test_connect_authentication_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """认证失败时，应转换为项目自己的认证异常。"""

    def fake_connect_handler(**connection_params):
        """模拟 Netmiko 判断用户名或密码错误。"""

        raise NetmikoAuthenticationException(
            "模拟 SSH 认证失败"
        )

    monkeypatch.setattr(
        ssh_device_module,
        "ConnectHandler",
        fake_connect_handler,
    )

    device = SSHDevice(
        name="r1",
        connection_params={
            "device_type": "cisco_ios",
            "host": "172.16.100.11",
            "username": "netlab",
            "password": "wrong-password",
        },
    )

    with pytest.raises(
        DeviceAuthenticationError,
        match="SSH 认证失败",
    ):
        device.connect()

    assert device.is_connected is False

class FakeConnection:
    """模拟 Netmiko 返回的连接对象。"""

    def __init__(self) -> None:
        self.disconnected = False

    def disconnect(self) -> None:
        """模拟断开连接。"""

        self.disconnected = True