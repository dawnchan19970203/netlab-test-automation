# NetLab Test Automation Framework

NetLab 是一个基于 Python、Pytest 和 Netmiko 开发的网络设备自动化测试框架。

项目使用 EVE-NG 构建虚拟网络环境，通过 SSH 控制真实网络设备 CLI，
实现设备管理、协议状态验证、故障注入、环境恢复、日志记录和测试报告生成。

## Features

- YAML 设备配置管理
- YAML 测试拓扑管理
- 基于 Netmiko 的 SSH 设备控制
- 查询命令与配置命令统一封装
- DeviceManager 统一管理设备连接
- Pytest Fixture 集成
- CleanupManager 自动恢复测试环境
- 自定义异常处理
- 运行日志记录
- pytest-html 测试报告
- 测试日志和报告自动归档
- OSPF Integration Test 示例

## Project Structure

```text
netlab-test/
├── artifacts/              # 历史测试运行归档
├── logs/                   # 当前运行日志
├── reports/                # HTML 测试报告
│
├── tests/
│   ├── integration/
│   │   ├── conftest.py
│   │   └── test_ospf.py
│   └── test_ssh_device.py
│
├── artifact_manager.py     # 测试结果归档
├── cleanup.py              # 环境恢复
├── config.py               # 设备配置读取
├── device_manager.py       # 设备统一管理
├── devices.yaml            # SSH 设备信息
├── exceptions.py           # 自定义异常
├── logger.py               # 日志配置
├── main.py                 # 框架统一运行入口
├── pytest.ini
├── requirements.txt
├── ssh_device.py           # 单台 SSH 设备控制
├── topology.py             # 拓扑配置读取
└── topology.yaml           # 测试拓扑信息
```

## Architecture

```text
                    main.py
                       |
                     Pytest
                       |
                  conftest.py
                  /         \
                 /           \
        DeviceManager    CleanupManager
              |                |
          SSHDevice         环境恢复
              |
           Netmiko
              |
        Network Device


devices.yaml
     |
  config.py
     |
DeviceManager


topology.yaml
     |
 topology.py
     |
 Test Cases
```

## Installation

建议使用 Python 3.11+。

安装依赖：

```bash
pip install -r requirements.txt
```

## Device Configuration

设备 SSH 信息保存在 `devices.yaml`：

```yaml
devices:
  r1:
    device_type: cisco_ios
    host: 172.16.100.11
    port: 22
    username: admin
    password: admin
```

## Topology Configuration

业务拓扑信息保存在 `topology.yaml`：

```yaml
links:
  r1_r2:
    r1:
      interface: GigabitEthernet0/1
      ip: 10.0.12.1

    r2:
      interface: GigabitEthernet0/0
      ip: 10.0.12.2

loopbacks:
  r1: 10.255.0.1
  r2: 10.255.0.2
```

## Running Tests

通过统一入口运行 Integration Tests：

```bash
python main.py
```

开发调试时也可以直接使用 Pytest：

```bash
pytest -s tests/integration
```

## Test Output

测试运行后会产生：

```text
logs/
```

保存运行日志。

```text
reports/
```

保存 HTML 测试报告。

```text
artifacts/
```

按照测试运行时间归档对应的日志和报告。

## Current OSPF Test Scenario

当前 EVE-NG 测试拓扑：

```text
Management Network
       |
      R1
       |
   10.0.12.0/30
       |
      R2
```

当前 OSPF Integration Test 已实现：

- OSPF Neighbor FULL 状态验证
- OSPF 路由学习验证
- 对端 Loopback 连通性验证
- 接口 Shutdown 故障注入
- 测试结束后的自动环境恢复

## Tech Stack

- Python
- Pytest
- Netmiko
- PyYAML
- EVE-NG
- Cisco IOS
- Git / GitHub