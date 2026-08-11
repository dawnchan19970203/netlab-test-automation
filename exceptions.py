"""NetLab 项目自定义异常。"""


class NetLabError(Exception):
    """NetLab 项目所有预期异常的基类。"""


class DeviceError(NetLabError):
    """所有设备操作异常的基类。"""


class DeviceConnectionError(DeviceError):
    """设备连接建立失败或连接中断。"""


class DeviceAuthenticationError(DeviceConnectionError):
    """设备用户名、密码或认证方式错误。"""


class DeviceStateError(DeviceError):
    """设备对象当前状态不允许执行操作。"""


class CommandExecutionError(DeviceError):
    """设备命令参数、发送或输出读取失败。"""