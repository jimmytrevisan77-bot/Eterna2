"""Simple startup verification script for Eterna modules."""

from __future__ import annotations

import json
from pathlib import Path

from backend import EternaCoreManager, IOSBridge, modules


def main() -> None:
    summary = {}

    memory = modules.EternaMemoryManager(Path("./storage/memory"))
    summary["memory"] = {
        "personal_count": len(memory.fetch_scope(memory.PERSONAL_SCOPE)),
        "professional_count": len(memory.fetch_scope(memory.PROFESSIONAL_SCOPE)),
    }

    emotions = modules.EmotionService()
    summary["emotion_service"] = emotions.service_status()

    system = modules.SystemControlService()
    snapshot = system.get_snapshot()
    summary["system_control"] = {
        "cpu_percent": snapshot.cpu_percent,
        "memory_percent": snapshot.memory_percent,
        "gpu_percent": snapshot.gpu_percent,
    }

    updates = modules.SelfUpdateManager(project_root=Path("."))
    summary["self_update_manager"] = {
        "backup_root": str(updates.backup_root),
    }

    enhancer = modules.ImageService()
    summary["image_service"] = enhancer.status()

    commerce = modules.CommerceManager()
    summary["commerce_manager"] = commerce.status().__dict__

    bridge = IOSBridge()
    summary["ios_bridge_ready"] = bridge.is_available

    security = modules.SecurityManager()
    summary["security_manager"] = security.status().__dict__

    orchestrator = modules.TaskOrchestrator()
    summary["task_orchestrator"] = orchestrator.status()

    llama = modules.LlamaService()
    summary["llama_service"] = llama.status()

    tts = modules.TTSService()
    summary["tts_service"] = tts.status()

    whisper = modules.WhisperService()
    summary["whisper_service"] = whisper.status()

    network = modules.NetworkManager()
    summary["network_manager"] = network.status()

    core = EternaCoreManager()
    summary["core_manager"] = core.heartbeat()

    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
