"""Ensure runtime dependencies for the Eterna2 suite are present."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path

EXPECTED_PYTHON = (3, 11)
EXPECTED_TORCH = "2.2.2"
EXPECTED_CUDA = "12.4"
REQUIRED_TOOLS = ["dotnet", "python", "pip"]
CONFIG_PATH = Path(__file__).resolve().parents[1] / "Config" / "AppConfig.json"


def _check_python() -> bool:
    return sys.version_info[:2] >= EXPECTED_PYTHON


def _check_torch() -> bool:
    try:
        import torch  # type: ignore
    except Exception:
        return False
    return torch.__version__.startswith(EXPECTED_TORCH) and torch.version.cuda.startswith(EXPECTED_CUDA)


def _check_tools() -> dict:
    return {tool: shutil.which(tool) is not None for tool in REQUIRED_TOOLS}


def _check_models() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data.get("models", {})


def main() -> int:
    report = {
        "python": _check_python(),
        "torch": _check_torch(),
        "tools": _check_tools(),
        "models": _check_models(),
        "platform": platform.platform(),
    }
    print(json.dumps(report, indent=2))
    return 0 if all(report["tools"].values()) and report["python"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
