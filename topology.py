"""负责读取测试拓扑配置。"""

from pathlib import Path
from typing import Any

import yaml


def load_topology(
    config_path: str | Path,
) -> dict[str, Any]:
    """读取 topology.yaml。"""

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"拓扑配置文件不存在：{path}"
        )

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "拓扑配置必须是字典。"
        )

    return data