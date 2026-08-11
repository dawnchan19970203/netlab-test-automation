# NetLab Test Automation Framework

基于 Python、Pytest 和 Netmiko 开发的网络设备自动化测试框架。

当前框架用于控制 EVE-NG 中的网络设备，并执行真实网络协议测试。

## Features

- YAML 设备配置管理
- SSH 网络设备控制
- DeviceManager 多设备统一管理
- 查询命令与配置命令封装
- Pytest Fixture 集成
- 自动环境恢复
- 日志记录
- HTML 测试报告
- 测试结果自动归档
- OSPF 真实设备测试示例

## Project Structure

```text
netlab-test/
├── artifacts/
├── logs/
├── reports/
├── tests/
│   ├── integration/
│   │   ├── conftest.py
│   │   └── test_ospf.py
│   └── test_ssh_device.py
│
├── artifact_manager.py
├── cleanup.py
├── config.py
├── device_manager.py
├── devices.yaml
├── exceptions.py
├── logger.py
├── main.py
├── pytest.ini
├── requirements.txt
├── ssh_device.py
├── topology.py
└── topology.yaml