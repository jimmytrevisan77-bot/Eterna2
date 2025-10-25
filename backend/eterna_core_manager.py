"""Core orchestration layer for the local Eterna2 stack."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Protocol


class LifecycleModule(Protocol):
    """Small protocol used to describe backend modules."""

    name: str

    def start(self) -> None:  # pragma: no cover - simple interface definition
        """Start background workers or allocate resources."""

    def stop(self) -> None:  # pragma: no cover - simple interface definition
        """Release resources and shutdown background workers."""

    def status(self) -> Dict[str, Any]:  # pragma: no cover - simple interface definition
        """Return a serialisable status payload for telemetry."""


class EternaCoreManager:
    """Coordinates all backend modules that power the local experience."""

    def __init__(self, config_path: Optional[Path] = None, log_dir: Optional[Path] = None) -> None:
        self._config_path = config_path or Path("config") / "AppConfig.json"
        self._log_dir = log_dir or Path("logs")
        self._config: Dict[str, Any] = {}
        self._modules: Dict[str, LifecycleModule] = {}
        self._logger = self._create_logger()
        self._load_config()

    def _create_logger(self) -> logging.Logger:
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / "core_manager.log"
        logger = logging.getLogger("EternaCoreManager")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _load_config(self) -> None:
        if not self._config_path.exists():
            self._logger.warning("Config file %s not found, using defaults", self._config_path)
            self._config = {
                "models": {},
                "network": {"allow_incoming": False, "pipe_name": "eterna_core_pipe"},
                "paths": {"memory_root": "config/Memory"},
            }
            return

        with self._config_path.open("r", encoding="utf-8") as handle:
            self._config = json.load(handle)
        self._logger.info("Configuration loaded from %s", self._config_path)

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    def register_module(self, module: LifecycleModule) -> None:
        self._modules[module.name] = module
        self._logger.info("Registered module: %s", module.name)

    def load_modules(self, modules: Iterable[LifecycleModule]) -> None:
        for module in modules:
            self.register_module(module)

    def start(self) -> None:
        for module in self._modules.values():
            try:
                module.start()
                self._logger.info("Started module %s", module.name)
            except Exception as exc:  # pragma: no cover - defensive logging
                self._logger.exception("Failed to start module %s: %s", module.name, exc)

    def stop(self) -> None:
        for module in self._modules.values():
            try:
                module.stop()
                self._logger.info("Stopped module %s", module.name)
            except Exception as exc:  # pragma: no cover - defensive logging
                self._logger.exception("Failed to stop module %s: %s", module.name, exc)

    def status_report(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {"config": self._config, "modules": {}}
        for name, module in self._modules.items():
            try:
                report["modules"][name] = module.status()
            except Exception as exc:  # pragma: no cover - defensive logging
                report["modules"][name] = {"error": str(exc)}
        return report


__all__ = ["EternaCoreManager", "LifecycleModule"]
