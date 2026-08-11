"""统一管理测试结束后的环境恢复动作。"""

import logging
from collections.abc import Callable
from typing import Any


class CleanupManager:
    """记录并执行测试结束后的恢复动作。"""

    def __init__(self) -> None:
        self._actions: list[
            tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]
        ] = []

        self._logger = logging.getLogger(
            "netlab.cleanup"
        )

    # 注册代办事项,不具体去执行
    def add(
        self,
        action: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """注册一个恢复动作。"""

        self._actions.append(
            (action, args, kwargs)
        )

    def run(self) -> None:
        """按照注册的相反顺序执行所有恢复动作。"""

        while self._actions:
            action, args, kwargs = self._actions.pop()

            try:
                action(*args, **kwargs)

            except Exception:
                self._logger.exception(
                    "执行环境恢复动作失败。"
                )