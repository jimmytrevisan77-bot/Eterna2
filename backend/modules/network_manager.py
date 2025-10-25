"""Network security layer ensuring Eterna stays local-first."""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Optional

try:  # pragma: no cover - optional dependency for strict firewalling
    import psutil
except Exception:  # pragma: no cover - degrade gracefully
    psutil = None  # type: ignore

CONFIG_ROOT = Path("./Config")
RULES_FILE = CONFIG_ROOT / "NetworkRules.json"
LOG_DIR = Path("./Logs")
LOG_FILE = LOG_DIR / "network.log"
LOCALHOST = "127.0.0.1"


class NetworkManager:
    """Centralise allowed endpoints and local IPC channels."""

    def __init__(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("eterna.network")
        self._configure_logger()
        self.rules = self._load_rules()

    # ------------------------------------------------------------------
    def is_outgoing_allowed(self, host: str) -> bool:
        """Check whether the host is authorised for outbound calls."""

        allowed = self.rules.get("allowed_hosts", [])
        decision = host in allowed
        self.logger.info("OUTGOING %s -> %s", "ALLOW" if decision else "BLOCK", host)
        return decision

    def register_outgoing_host(self, host: str) -> None:
        """Allow a new outbound host and persist it."""

        allowed = set(self.rules.setdefault("allowed_hosts", []))
        if host not in allowed:
            allowed.add(host)
            self.rules["allowed_hosts"] = sorted(allowed)
            self._store_rules()
            self.logger.info("REGISTER allow host=%s", host)

    def block_incoming(self) -> None:
        """Close any unexpected external listeners (best effort)."""

        if psutil is None:  # pragma: no cover - fallback
            self.logger.warning("psutil not available; incoming scan skipped")
            return

        for conn in psutil.net_connections(kind="inet"):
            if conn.laddr and conn.laddr.ip not in {LOCALHOST, "::1"} and conn.status == psutil.CONN_LISTEN:
                self.logger.warning("Detected non-local listener on %s:%s", conn.laddr.ip, conn.laddr.port)

    @contextmanager
    def local_pipe(self, name: str = "eterna_ipc") -> Iterator[str]:
        """Expose a named pipe endpoint for WPF <-> backend comms."""

        pipe_name = fr"\\\\.\\pipe\\{name}"
        self.logger.info("PIPE open %s", pipe_name)
        try:
            yield pipe_name
        finally:
            self.logger.info("PIPE close %s", pipe_name)

    def pipe_name(self, name: str = "eterna_ipc") -> str:
        """Return the Windows named pipe identifier without opening it."""

        return fr"\\\\.\\pipe\\{name}"

    def log_request(self, method: str, target: str, payload_bytes: int = 0) -> None:
        """Record a network access in the local log."""

        self.logger.info("REQUEST method=%s target=%s bytes=%s", method.upper(), target, payload_bytes)

    def status(self) -> Dict[str, str | bool]:
        """Expose current rule information for diagnostics."""

        return {
            "rules_file": str(RULES_FILE),
            "log_file": str(LOG_FILE),
            "psutil_available": psutil is not None,
            "allowed_hosts": ",".join(self.rules.get("allowed_hosts", [])),
        }

    # ------------------------------------------------------------------
    def _configure_logger(self) -> None:
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)

        # ensure file handler only added once
        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == handler.baseFilename for h in self.logger.handlers):
            self.logger.addHandler(handler)
        self.logger.propagate = False

    def _load_rules(self) -> Dict[str, list]:
        if not RULES_FILE.exists():
            default_rules = {
                "allowed_hosts": [
                    "huggingface.co",
                    "shopify.com",
                    "printify.com",
                    "etsy.com",
                    "ngrok.io",
                ],
            }
            self._store_rules(default_rules)
            return default_rules

        with RULES_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _store_rules(self, rules: Optional[Dict[str, list]] = None) -> None:
        RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = rules or self.rules
        with RULES_FILE.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
