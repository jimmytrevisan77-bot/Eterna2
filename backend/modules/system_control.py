"""System control utilities for Eterna."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

try:  # pragma: no cover - optional dependency
    import psutil
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import pyautogui
except ImportError:  # pragma: no cover
    pyautogui = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from openrgb import OpenRGBClient
    from openrgb.utils import RGBColor
except ImportError:  # pragma: no cover
    OpenRGBClient = None  # type: ignore
    RGBColor = None  # type: ignore


@dataclass
class SystemSnapshot:
    cpu_percent: float
    memory_percent: float
    gpu_percent: Optional[float] = None


class SystemControlService:
    """Expose automation primitives and telemetry for the UI."""

    def __init__(self) -> None:
        self._openrgb: Optional[OpenRGBClient] = None

    def get_snapshot(self) -> SystemSnapshot:
        cpu = float(psutil.cpu_percent(interval=None)) if psutil else 0.0
        memory = float(psutil.virtual_memory().percent) if psutil else 0.0
        gpu = self._probe_gpu()
        return SystemSnapshot(cpu_percent=cpu, memory_percent=memory, gpu_percent=gpu)

    def move_mouse(self, x: int, y: int) -> bool:
        if pyautogui is None:  # pragma: no cover
            return False
        try:
            pyautogui.moveTo(x, y)
            return True
        except Exception:
            return False

    def type_text(self, text: str) -> bool:
        if pyautogui is None:  # pragma: no cover
            return False
        try:
            pyautogui.typewrite(text)
            return True
        except Exception:
            return False

    def set_rgb_color(self, r: int, g: int, b: int) -> bool:
        if OpenRGBClient is None or RGBColor is None:  # pragma: no cover
            return False
        try:
            if self._openrgb is None:
                self._openrgb = OpenRGBClient()
            color = RGBColor(r, g, b)
            for device in self._openrgb.devices:
                device.set_color(color)
            return True
        except Exception:
            return False

    def _probe_gpu(self) -> Optional[float]:
        if psutil is None:  # pragma: no cover
            return None
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if not temps:
                    return None
            # Without a GPU monitor dependency we expose utilisation via NVML if available later.
            return None
        except Exception:
            return None

    def to_json(self) -> str:
        snapshot = self.get_snapshot()
        return json.dumps(snapshot.__dict__)

    def status(self) -> dict:
        """Return telemetry about available control backends."""

        return {
            "psutil_available": psutil is not None,
            "pyautogui_available": pyautogui is not None,
            "openrgb_available": OpenRGBClient is not None,
        }


__all__ = ["SystemControlService", "SystemSnapshot"]
