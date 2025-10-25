"""Text-to-speech output for the local Eterna2 assistant."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from backend.eterna_core_manager import LifecycleModule

try:
    from TTS.api import TTS
except ModuleNotFoundError:  # pragma: no cover
    TTS = None  # type: ignore


class TTSService(LifecycleModule):
    """Wraps a Coqui TTS model for offline speech synthesis."""

    name = "tts_service"

    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2", output_dir: Optional[Path] = None) -> None:
        self._model_name = model_name
        self._output_dir = output_dir or Path("outputs") / "tts"
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._tts: Optional[TTS] = None  # type: ignore[assignment]
        self._logger = logging.getLogger("TTSService")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def start(self) -> None:
        if TTS is None:
            self._logger.warning("Coqui TTS not installed; speech synthesis disabled")
            return
        self._logger.info("Loading TTS model %s", self._model_name)
        self._tts = TTS(model_name=self._model_name)

    def stop(self) -> None:
        self._tts = None

    def status(self) -> Dict[str, Any]:
        return {
            "model_name": self._model_name,
            "loaded": self._tts is not None,
            "output_dir": str(self._output_dir),
        }

    def speak(self, text: str, speaker_wav: Optional[Path] = None) -> Path:
        if self._tts is None:
            raise RuntimeError("TTS model is not loaded")
        output_path = self._output_dir / "utterance.wav"
        self._logger.info("Synthesising speech -> %s", output_path)
        kwargs: Dict[str, Any] = {"text": text, "file_path": str(output_path)}
        if speaker_wav:
            kwargs["speaker_wav"] = str(speaker_wav)
        self._tts.tts_to_file(**kwargs)
        return output_path


__all__ = ["TTSService"]
