"""Network governance layer enforcing the offline-first policy."""

from __future__ import annotations

import json
import logging
import socket
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

from backend.eterna_core_manager import LifecycleModule


class NetworkManager(LifecycleModule):
    """Controls outbound allow-lists and records every network interaction."""

    name = "network_manager"

    def __init__(self, rules_path: Optional[Path] = None, log_dir: Optional[Path] = None) -> None:
        self._rules_path = rules_path or Path("config") / "NetworkRules.json"
        self._log_dir = log_dir or Path("logs")
        self._logger = self._create_logger()
        self._rules: Dict[str, Any] = {}
        self._audit_entries: List[Dict[str, Any]] = []

    def _create_logger(self) -> logging.Logger:
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / "network.log"
        logger = logging.getLogger("NetworkManager")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def start(self) -> None:
        self._rules = self._load_rules()
        self._logger.info(
            "Network manager initialised with %s outbound rules",
            len(self._rules.get("allowed_hosts", [])),
        )

    def stop(self) -> None:
        self._logger.info("Network manager stopped")

    def status(self) -> Dict[str, Any]:
        return {
            "allowed_hosts": self._rules.get("allowed_hosts", []),
            "allow_incoming": self._rules.get("allow_incoming", False),
            "pipe_name": self._rules.get("pipe_name"),
            "audit_entries": len(self._audit_entries),
        }

    def _load_rules(self) -> Dict[str, Any]:
        if not self._rules_path.exists():
            self._logger.warning("Missing network rules file %s", self._rules_path)
            return {
                "allow_incoming": False,
                "pipe_name": "eterna_core_pipe",
                "allowed_hosts": [
                    "huggingface.co",
                    "shopify.com",
                    "printify.com",
                    "etsy.com",
                ],
            }
        with self._rules_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def is_host_allowed(self, host: str) -> bool:
        allowed = set(self._rules.get("allowed_hosts", []))
        result = host in allowed
        self._logger.info("Checked host %s -> %s", host, result)
        return result

    def validate_outbound(self, url: str) -> bool:
        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            raise ValueError(f"Invalid URL: {url}")
        if not self.is_host_allowed(host):
            self._logger.error("Blocked outbound request to %s", url)
            return False
        self._record_audit({"direction": "outbound", "url": url})
        return True

    def record_inbound_attempt(self, source: str) -> None:
        if self._rules.get("allow_incoming"):
            self._record_audit({"direction": "inbound", "source": source, "accepted": True})
            self._logger.info("Allowed inbound connection from %s", source)
        else:
            self._record_audit({"direction": "inbound", "source": source, "accepted": False})
            self._logger.warning("Blocked inbound connection from %s", source)

    def _record_audit(self, entry: Dict[str, Any]) -> None:
        self._audit_entries.append(entry)

    def enforce_local_socket(self) -> socket.socket:
        pipe_name = self._rules.get("pipe_name", "eterna_core_pipe")
        sock = socket.socket(socket.AF_UNIX)
        try:
            sock.bind(f"\0{pipe_name}")
        except OSError as exc:  # pragma: no cover - environment specific
            self._logger.warning("Named pipe %s unavailable: %s", pipe_name, exc)
        self._logger.info("Local socket %s prepared", pipe_name)
        return sock

    def export_audit(self) -> Iterable[Dict[str, Any]]:
        return list(self._audit_entries)


__all__ = ["NetworkManager"]
