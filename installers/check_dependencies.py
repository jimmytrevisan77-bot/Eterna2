"""Checks Python dependencies required for the local deployment."""

from __future__ import annotations

import importlib
from typing import List

REQUIRED_MODULES: List[str] = [
    "torch",
    "transformers",
    "faster_whisper",
    "TTS",
    "realesrgan",
    "rembg",
    "tinydb",
    "psutil",
    "pyautogui",
    "openrgb",
    "python_socketio",
]


def main() -> None:
    missing = []
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            missing.append(module)
    if missing:
        print("Missing modules:\n - " + "\n - ".join(missing))
    else:
        print("All dependencies are available.")


if __name__ == "__main__":
    main()
