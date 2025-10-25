"""Local Socket.IO bridge dedicated to the iOS remote companion."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

try:  # Optional import to keep startup light-weight
    import socketio
except ModuleNotFoundError:  # pragma: no cover - import guard for environments without python-socketio
    socketio = None  # type: ignore


class IOSBridge:
    """Manages the secure Socket.IO session used by the iOS companion."""

    def __init__(self, config_path: Optional[Path] = None, log_dir: Optional[Path] = None) -> None:
        self._config_path = config_path or Path("Config") / "AppConfig.json"
        self._log_dir = log_dir or Path("Logs")
        self._logger = self._create_logger()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._client: Optional["socketio.AsyncClient"] = None
        self._endpoint: Optional[str] = None
        self._token: Optional[str] = None
        self._load_config()

    def _create_logger(self) -> logging.Logger:
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / "ios_bridge.log"
        logger = logging.getLogger("IOSBridge")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _load_config(self) -> None:
        if not self._config_path.exists():
            self._logger.warning("Missing configuration file %s", self._config_path)
            return
        with self._config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        ios_cfg = data.get("ios", {})
        self._endpoint = ios_cfg.get("endpoint")
        self._token = ios_cfg.get("token")

    def _ensure_client(self) -> "socketio.AsyncClient":
        if socketio is None:  # pragma: no cover - runtime guard
            raise RuntimeError("python-socketio is required to use the iOS bridge")
        if self._client is None:
            self._client = socketio.AsyncClient()
            self._client.on("connect", self._on_connect)
            self._client.on("disconnect", self._on_disconnect)
        return self._client

    async def connect(self) -> None:
        if not self._endpoint:
            raise RuntimeError("iOS bridge endpoint is not configured")
        client = self._ensure_client()
        headers = {"Authorization": f"Bearer {self._token}"} if self._token else None
        self._logger.info("Connecting to iOS endpoint %s", self._endpoint)
        await client.connect(self._endpoint, headers=headers, transports=["websocket"])

    async def disconnect(self) -> None:
        if self._client is None:
            return
        self._logger.info("Disconnecting from iOS endpoint")
        await self._client.disconnect()

    async def emit_status(self, payload: Dict[str, Any]) -> None:
        if self._client is None or not self._client.connected:
            raise RuntimeError("iOS bridge is not connected")
        await self._client.emit("eterna_status", payload)

    def is_connected(self) -> bool:
        return bool(self._client and self._client.connected)

    def _on_connect(self) -> None:  # pragma: no cover - callback wiring
        self._logger.info("iOS bridge connected")

    def _on_disconnect(self) -> None:  # pragma: no cover - callback wiring
        self._logger.info("iOS bridge disconnected")

    def connect_blocking(self) -> None:
        """Helper used by the CLI tooling to establish the session synchronously."""

        async def runner() -> None:
            await self.connect()

        self._loop.run_until_complete(runner())

    def disconnect_blocking(self) -> None:
        if self._client is None:
            return

        async def runner() -> None:
            await self.disconnect()

        self._loop.run_until_complete(runner())


__all__ = ["IOSBridge"]
