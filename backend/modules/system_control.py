"""System control helpers for automation and telemetry."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

try:  # Optional dependencies for runtime automation
    import psutil
except ModuleNotFoundError:  # pragma: no cover
    psutil = None  # type: ignore

try:
    import pyautogui
except ModuleNotFoundError:  # pragma: no cover
    pyautogui = None  # type: ignore

try:
    from openrgb import OpenRGBClient
except ModuleNotFoundError:  # pragma: no cover
    OpenRGBClient = None  # type: ignore

from backend.eterna_core_manager import LifecycleModule


class SystemControl(LifecycleModule):
    """Collects telemetry and exposes automation hooks."""

    name = "system_control"

    def __init__(self, log_dir: Optional[str] = None) -> None:
        self._log_dir = log_dir
        self._client: Optional[Any] = None
        self._logger = logging.getLogger("SystemControl")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def start(self) -> None:
        if OpenRGBClient is not None:
            try:
                self._client = OpenRGBClient()  # type: ignore[call-arg]
                self._logger.info("Connected to OpenRGB server")
            except Exception as exc:  # pragma: no cover - external dependency
                self._logger.warning("Unable to connect to OpenRGB: %s", exc)
        if pyautogui is None:
            self._logger.warning("PyAutoGUI not installed; automation disabled")

    def stop(self) -> None:
        if self._client is not None:
            try:
                self._client.disconnect()  # type: ignore[attr-defined]
                self._logger.info("Disconnected from OpenRGB")
            except Exception as exc:  # pragma: no cover
                self._logger.warning("Failed to disconnect OpenRGB: %s", exc)
        self._client = None

    def status(self) -> Dict[str, Any]:
        return {
            "openrgb": self._client is not None,
            "automation": pyautogui is not None,
            "telemetry": psutil is not None,
        }

    def get_telemetry(self) -> Dict[str, Any]:
        if psutil is None:
            raise RuntimeError("psutil is required to gather telemetry")
        return {
            "cpu": psutil.cpu_percent(interval=0.1),
            "gpu": None,  # Placeholder for dedicated GPU integration
            "memory": psutil.virtual_memory()._asdict(),
        }

    def move_mouse(self, x: int, y: int) -> None:
        if pyautogui is None:
            raise RuntimeError("PyAutoGUI is required for automation")
        pyautogui.moveTo(x, y)


__all__ = ["SystemControl"]
