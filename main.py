"""NetLab 自动化测试运行入口。"""

from pathlib import Path

import pytest

from artifact_manager import archive_test_artifacts
from logger import setup_logging


PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = PROJECT_DIR / "logs"


def main() -> int:
    """运行测试并归档测试结果。"""

    setup_logging(LOG_DIR)

    exit_code = pytest.main([
        str(PROJECT_DIR / "tests" / "integration"),
    ])

    run_dir = archive_test_artifacts()

    print(f"\n测试结果已归档：{run_dir}")

    return int(exit_code)


if __name__ == "__main__":
    raise SystemExit(main())