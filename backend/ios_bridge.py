"""Socket.IO bridge between the Windows host and iOS client."""

from __future__ import annotations

from typing import Callable

try:  # pragma: no cover - optional dependency
    import socketio
except ImportError:  # pragma: no cover
    socketio = None  # type: ignore[assignment]


class IOSBridge:
    """Manage realtime communication with the remote iOS companion."""

    def __init__(self, namespace: str = "/eterna") -> None:
        self.namespace = namespace
        if socketio is None:  # pragma: no cover
            self._server = None
            self._app_factory = None
        else:
            self._server = socketio.AsyncServer(async_mode="asgi")
            self._app_factory = socketio.ASGIApp

    def create_app(self):  # pragma: no cover - runtime integration
        """Return a minimal ASGI application without external web frameworks."""

        if self._server is None:
            raise RuntimeError("python-socketio is not installed")
        if self._app_factory is None:
            raise RuntimeError("socketio.ASGIApp factory unavailable")

        return self._app_factory(self._server, socketio_path="socket.io")

    def emit_status(self, event: str, data: dict) -> bool:
        if self._server is None:  # pragma: no cover
            return False
        try:
            self._server.emit(event, data, namespace=self.namespace)
            return True
        except Exception:
            return False

    def register_handler(self, event: str, handler: Callable):  # pragma: no cover - dynamic wiring
        if self._server is None:
            return False
        self._server.on(event, handler, namespace=self.namespace)
        return True

    @property
    def is_available(self) -> bool:
        return self._server is not None

    @property
    def server(self):  # pragma: no cover - debugging helper
        return self._server


__all__ = ["IOSBridge"]
