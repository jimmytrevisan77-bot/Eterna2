"""Verifies that all backend modules are importable and initialisable."""

from __future__ import annotations

import importlib
import sys
from typing import List, Tuple

MODULES: List[Tuple[str, str]] = [
    ("backend", "eterna_core_manager"),
    ("backend", "ios_bridge"),
    ("backend.modules", "network_manager"),
    ("backend.modules", "memory_manager"),
    ("backend.modules", "emotion_service"),
    ("backend.modules", "system_control"),
    ("backend.modules", "llama_service"),
    ("backend.modules", "whisper_service"),
    ("backend.modules", "tts_service"),
    ("backend.modules", "image_service"),
    ("backend.modules", "commerce_manager"),
    ("backend.modules", "security_manager"),
    ("backend.modules", "self_update_manager"),
    ("backend.modules", "task_orchestrator"),
]


def main() -> int:
    errors = 0
    for package, name in MODULES:
        module_path = f"{package}.{name}"
        try:
            importlib.import_module(module_path)
        except Exception as exc:  # pragma: no cover - diagnostic script
            errors += 1
            print(f"[FAIL] {module_path}: {exc}")
        else:
            print(f"[OK] {module_path}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
