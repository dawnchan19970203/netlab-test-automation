"""连接 EVE-NG 真实设备的集成测试。"""

import pytest

from ssh_device import SSHDevice


@pytest.mark.integration
@pytest.mark.parametrize(
    "command, expected_text",
    [
        (
            "show ip interface brief",
            "Vlan100",
        ),
        (
            "show vlan brief",
            "100",
        ),
    ],
)
def test_real_show_command(
    real_r1: SSHDevice,
    command: str,
    expected_text: str,
) -> None:
    """执行不同的 show 命令，并检查预期内容。"""

    output = real_r1.execute_command(
        command=command,
        read_timeout=30,
    )

    assert output.strip()
    assert expected_text in output

@pytest.mark.integration
def test_temporary_loopback_configuration(
    real_r1: SSHDevice,
    temporary_loopback: dict[str, str],
) -> None:
    """检查临时 Loopback 配置已经生效。"""

    interface_name = temporary_loopback["name"]
    expected_ip = temporary_loopback["ip"]

    output = real_r1.execute_command(
        command=(
            f"show running-config "
            f"interface {interface_name}"
        ),
        read_timeout=30,
    )

    assert f"interface {interface_name}" in output
    assert "description NETLAB_PYTEST_TEMP" in output
    assert expected_ip in output


