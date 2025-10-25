"""Emotion analytics module combining visual and vocal cues."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from backend.eterna_core_manager import LifecycleModule

try:  # Optional dependencies
    from deepface import DeepFace
except ModuleNotFoundError:  # pragma: no cover
    DeepFace = None  # type: ignore

try:
    from speechbrain.inference.interfaces import foreign_class
except ModuleNotFoundError:  # pragma: no cover
    foreign_class = None  # type: ignore


class EmotionService(LifecycleModule):
    """Evaluates emotion state from camera frames and audio samples."""

    name = "emotion_service"

    def __init__(self, model_dir: Optional[Path] = None, log_dir: Optional[Path] = None) -> None:
        self._model_dir = model_dir or Path("models") / "emotion"
        self._log_dir = log_dir or Path("logs")
        self._logger = self._create_logger()
        self._speechbrain: Any = None

    def _create_logger(self) -> logging.Logger:
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / "emotion.log"
        logger = logging.getLogger("EmotionService")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def start(self) -> None:
        if foreign_class is not None:
            self._speechbrain = foreign_class(
                source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
                pymodule_file="custom_interface.py",
                classname="CustomEmotionRecognition",
                savedir=str(self._model_dir / "speechbrain"),
            )
            self._logger.info("Loaded SpeechBrain emotion model")
        else:
            self._logger.warning("SpeechBrain not installed; vocal emotion detection disabled")
        if DeepFace is None:
            self._logger.warning("DeepFace not installed; visual emotion detection disabled")
        else:
            self._logger.info("DeepFace available for emotion detection")

    def stop(self) -> None:
        self._speechbrain = None

    def status(self) -> Dict[str, Any]:
        return {
            "speechbrain": bool(self._speechbrain),
            "deepface": DeepFace is not None,
        }

    def analyse_frame(self, image_path: Path) -> Dict[str, Any]:
        if DeepFace is None:
            raise RuntimeError("DeepFace is required for visual emotion analysis")
        result = DeepFace.analyze(img_path=str(image_path), actions=["emotion"], enforce_detection=False)
        self._logger.info("Analysed frame %s", image_path)
        return result  # type: ignore[return-value]

    def analyse_audio(self, audio_path: Path) -> Dict[str, Any]:
        if self._speechbrain is None:
            raise RuntimeError("SpeechBrain emotion model is not initialised")
        scores, emotion = self._speechbrain.classify_file(str(audio_path))
        self._logger.info("Analysed audio %s -> %s", audio_path, emotion)
        return {"scores": scores, "emotion": emotion}


__all__ = ["EmotionService"]
