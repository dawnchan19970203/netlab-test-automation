"""使用 Netmiko 操作网络设备的 SSH 连接。"""

import logging
from types import TracebackType
from typing import Any

from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    ReadTimeout,
)

from exceptions import (
    CommandExecutionError,
    DeviceAuthenticationError,
    DeviceConnectionError,
    DeviceStateError,
)


class SSHDevice:
    """表示一台通过 SSH 管理的网络设备。"""

    def __init__(
        self,
        name: str,
        connection_params: dict[str, Any],
    ) -> None:
        self.name = name
        self._connection_params = dict(connection_params)
        self._connection: BaseConnection | None = None

        self._logger = logging.getLogger(
            f"netlab.device.{name}"
        )

    @property
    def is_connected(self) -> bool:
        """返回当前对象是否持有 SSH 连接。"""

        return self._connection is not None

    def connect(self) -> None:
        """建立 SSH 连接。"""

        if self._connection is not None:
            self._logger.warning(
                "设备已经连接，不重复建立连接。"
            )
            return

        host = self._connection_params.get(
            "host",
            "unknown",
        )
        port = self._connection_params.get(
            "port",
            22,
        )

        self._logger.info(
            "正在连接设备，host=%s，port=%s",
            host,
            port,
        )

        try:
            self._connection = ConnectHandler(
                **self._connection_params
            )

        except NetmikoAuthenticationException as exc:
            raise DeviceAuthenticationError(
                f"设备 {self.name!r} SSH 认证失败。"
            ) from exc

        except NetmikoTimeoutException as exc:
            raise DeviceConnectionError(
                f"连接设备 {self.name!r} 超时，"
                f"目标地址为 {host}:{port}。"
            ) from exc

        self._logger.info("SSH 连接成功。")

    def get_prompt(self) -> str:
        """获取设备当前 CLI 提示符。"""

        connection = self._require_connection()
        return connection.find_prompt()

    def execute_command(
        self,
        command: str,
        read_timeout: float = 30,
    ) -> str:
        """执行一条查询命令并返回字符串输出。"""

        # 参数校验放在连接检查前，
        # 这样空命令本身会得到明确错误。
        command = command.strip()

        if not command:
            raise CommandExecutionError(
                "设备命令不能为空。"
            )

        if read_timeout <= 0:
            raise CommandExecutionError(
                "read_timeout 必须大于 0。"
            )

        connection = self._require_connection()

        self._logger.info(
            "正在执行命令：%s",
            command,
        )

        try:
            output = connection.send_command(
                command,
                read_timeout=read_timeout,
            )

        except ReadTimeout as exc:
            raise CommandExecutionError(
                f"设备 {self.name!r} 执行命令超时："
                f"{command!r}"
            ) from exc

        except NetmikoTimeoutException as exc:
            raise DeviceConnectionError(
                f"设备 {self.name!r} 执行命令时连接异常："
                f"{command!r}"
            ) from exc

        self._logger.info(
            "命令执行完成，返回字符数：%d",
            len(output),
        )

        return output

    def execute_config(
        self,
        commands: list[str],
        read_timeout: float = 30,
    ) -> str:
        """向设备发送一组配置命令。"""

        clean_commands = [
            command.strip()
            for command in commands
            if command.strip()
        ]

        if not clean_commands:
            raise CommandExecutionError(
                "设备配置命令不能为空。"
            )

        connection = self._require_connection()

        try:
            output = connection.send_config_set(
                config_commands=clean_commands,
                read_timeout=read_timeout,
            )

            self._logger.info(
                "设备 %r 配置命令执行完成：%s",
                self.name,
                clean_commands,
            )

            return output

        except ReadTimeout as exc:
            raise CommandExecutionError(
                f"设备 {self.name!r} 执行配置命令超时。"
            ) from exc

    def disconnect(self) -> None:
        """断开 SSH 连接。"""

        connection = self._connection

        if connection is None:
            return

        try:
            connection.disconnect()
            self._logger.info("SSH 连接已断开。")

        except Exception:
            # 清理异常只记录，不覆盖原始业务异常
            self._logger.exception(
                "断开 SSH 连接时发生异常。"
            )

        finally:
            self._connection = None

    def _require_connection(self) -> BaseConnection:
        """返回连接；未连接时抛出项目异常。"""

        if self._connection is None:
            raise DeviceStateError(
                f"设备 {self.name!r} 尚未建立 SSH 连接。"
            )

        return self._connection

    def __enter__(self) -> "SSHDevice":
        """进入 with 时建立连接。"""

        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """离开 with 时断开连接。"""

        self.disconnect()