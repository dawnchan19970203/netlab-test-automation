"""负责归档每次测试运行产生的日志和报告。"""

from datetime import datetime
from pathlib import Path
import shutil


def archive_test_artifacts() -> Path:
    """将当前测试日志和报告复制到独立运行目录。"""

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    run_dir = Path("artifacts") / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    files = [
        Path("logs/netlab.log"),
        Path("reports/report.html"),
    ]

    for file_path in files:
        if file_path.is_file():
            shutil.copy2(
                file_path,
                run_dir / file_path.name,
            )

    return run_dir