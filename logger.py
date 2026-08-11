"""项目日志配置。"""

import logging
from pathlib import Path


def setup_logging(
    log_dir: str | Path,
    level: int = logging.INFO,
) -> None:
    """
    配置 NetLab 日志。

    日志会同时输出到：
    1. 控制台
    2. logs/netlab.log
    """

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # netlab 是本项目所有日志器的父日志器
    logger = logging.getLogger("netlab")
    logger.setLevel(level)

    # 日志由当前 logger 自己处理，
    # 不再继续传播给 Python 根日志器
    logger.propagate = False

    # 防止 setup_logging() 被重复调用时添加重复 Handler
    if logger.handlers:
        return

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # 文件输出
    file_handler = logging.FileHandler(
        filename=log_path / "netlab.log",
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)