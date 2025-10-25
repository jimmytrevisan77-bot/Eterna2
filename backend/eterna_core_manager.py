"""High level orchestrator wiring all backend capabilities together."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from .ios_bridge import IOSBridge
from .modules import (
    CommerceManager,
    EmotionService,
    EternaMemoryManager,
    ImageService,
    LlamaService,
    NetworkManager,
    SecurityManager,
    SelfUpdateManager,
    SystemControlService,
    TTSService,
    TaskOrchestrator,
    WhisperService,
)


class EternaCoreManager:
    """Provide a unified facade consumed by the desktop UI."""

    def __init__(self, project_root: Path | str = Path(".")) -> None:
        self.memory = EternaMemoryManager()
        self.emotions = EmotionService()
        self.system = SystemControlService()
        self.updates = SelfUpdateManager(project_root=project_root)
        self.images = ImageService()
        self.llm = LlamaService()
        self.tts = TTSService()
        self.whisper = WhisperService()
        self.network = NetworkManager()
        self.commerce = CommerceManager()
        self.ios = IOSBridge()
        self.security = SecurityManager()
        self.tasks = TaskOrchestrator()

    def heartbeat(self) -> Dict[str, Dict[str, bool] | Dict[str, str] | Dict[str, int] | Dict[str, float]]:
        """Expose service availability for diagnostics and startup checks."""

        return {
            "memory": {
                "professional_records": len(self.memory.fetch_scope(self.memory.PROFESSIONAL_SCOPE)),
                "personal_records": len(self.memory.fetch_scope(self.memory.PERSONAL_SCOPE)),
            },
            "emotions": self.emotions.service_status(),
            "system": self.system.status(),
            "images": self.images.status(),
            "llm": self.llm.status(),
            "tts": self.tts.status(),
            "whisper": self.whisper.status(),
            "network": self.network.status(),
            "commerce": self.commerce.status().__dict__,
            "security": self.security.status().__dict__,
            "tasks": self.tasks.status(),
        }

    def prepare_startup(self) -> Dict[str, Optional[str]]:
        """Run lightweight initialisation routines."""

        otp = self.security.current_otp()
        self.network.block_incoming()
        return {
            "otp": otp,
            "scheduler": "running" if self.tasks.scheduler else None,
            "pipe": self.network.pipe_name(),
        }


__all__ = ["EternaCoreManager"]
