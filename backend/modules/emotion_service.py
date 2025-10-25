"""Emotion analysis service combining DeepFace and SpeechBrain when available."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

try:  # pragma: no cover - optional dependency
    from deepface import DeepFace
except ImportError:  # pragma: no cover
    DeepFace = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from speechbrain.pretrained import EncoderClassifier
except ImportError:  # pragma: no cover
    EncoderClassifier = None  # type: ignore


@dataclass
class EmotionSnapshot:
    """Unified snapshot combining visual and vocal estimations."""

    dominant_emotion: str
    confidence: float
    source: str


class EmotionService:
    """Provide emotional state estimation to the UI."""

    def __init__(self, models_dir: Path | str = "./storage/models") -> None:
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._voice_classifier = None
        if EncoderClassifier is not None:  # pragma: no cover - optional branch
            try:
                self._voice_classifier = EncoderClassifier.from_hparams(
                    source="speechbrain/emotion-recognition-wav2vec2", savedir=str(self.models_dir / "speechbrain")
                )
            except Exception:
                self._voice_classifier = None

    def analyse_face(self, image_path: Path | str) -> Optional[EmotionSnapshot]:
        if DeepFace is None:  # pragma: no cover
            return None

        try:  # pragma: no cover - depends on heavy model
            analysis = DeepFace.analyze(img_path=str(image_path), actions=["emotion"], enforce_detection=False)
            dominant = analysis["dominant_emotion"]
            confidence = max(analysis.get("emotion", {}).values() or [0.0])
            return EmotionSnapshot(dominant, float(confidence), source="vision")
        except Exception:
            return None

    def analyse_voice(self, wav_path: Path | str) -> Optional[EmotionSnapshot]:
        if self._voice_classifier is None:  # pragma: no cover
            return None

        try:  # pragma: no cover - depends on heavy model
            scores, index = self._voice_classifier.classify_file(str(wav_path))
            label = self._voice_classifier.hparams.label_encoder.decode_ndim(index)
            confidence = float(scores.max().item()) if hasattr(scores, "max") else 0.0
            return EmotionSnapshot(label, confidence, source="voice")
        except Exception:
            return None

    def merge_signals(
        self,
        text_sentiment: Optional[EmotionSnapshot],
        face_snapshot: Optional[EmotionSnapshot],
        voice_snapshot: Optional[EmotionSnapshot],
    ) -> EmotionSnapshot:
        """Merge different modalities prioritising the most confident measurement."""

        candidates = [snap for snap in (text_sentiment, face_snapshot, voice_snapshot) if snap]
        if not candidates:
            return EmotionSnapshot("neutre", 0.0, source="synthetic")

        best = max(candidates, key=lambda snap: snap.confidence)
        return EmotionSnapshot(best.dominant_emotion, best.confidence, source=best.source)

    def service_status(self) -> Dict[str, bool]:
        """Expose readiness for diagnostics."""

        return {
            "deepface_available": DeepFace is not None,
            "speechbrain_available": self._voice_classifier is not None,
        }


__all__ = ["EmotionService", "EmotionSnapshot"]
