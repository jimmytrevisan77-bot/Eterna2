"""Speech-to-text service backed by local Whisper models."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from backend.eterna_core_manager import LifecycleModule

try:
    from faster_whisper import WhisperModel
except ModuleNotFoundError:  # pragma: no cover
    WhisperModel = None  # type: ignore


class WhisperService(LifecycleModule):
    """Encapsulates automatic speech recognition for offline use."""

    name = "whisper_service"

    def __init__(self, model_size: str = "medium", device: Optional[str] = None, compute_type: str = "int8") -> None:
        self._model_size = model_size
        self._device = device or "cuda"
        self._compute_type = compute_type
        self._model: Optional[WhisperModel] = None  # type: ignore[assignment]
        self._logger = logging.getLogger("WhisperService")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def start(self) -> None:
        if WhisperModel is None:
            self._logger.warning("faster-whisper not installed; ASR disabled")
            return
        self._logger.info("Loading Whisper %s model on %s", self._model_size, self._device)
        self._model = WhisperModel(self._model_size, device=self._device, compute_type=self._compute_type)

    def stop(self) -> None:
        self._model = None

    def status(self) -> Dict[str, Any]:
        return {
            "model_size": self._model_size,
            "device": self._device,
            "loaded": self._model is not None,
        }

    def transcribe(self, audio_path: Path) -> Dict[str, Any]:
        if self._model is None:
            raise RuntimeError("Whisper model is not loaded")
        segments, info = self._model.transcribe(str(audio_path))
        text = "".join(segment.text for segment in segments)
        self._logger.info("Transcribed %s", audio_path)
        return {"text": text, "language": info.language, "duration": info.duration}


__all__ = ["WhisperService"]
