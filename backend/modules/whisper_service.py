"""Speech-to-text helper built on Whisper or SpeechBrain."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:  # pragma: no cover - optional dependency
    import whisper
except Exception:  # pragma: no cover - degrade gracefully
    whisper = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from speechbrain.pretrained import EncoderDecoderASR
except Exception:  # pragma: no cover - degrade gracefully
    EncoderDecoderASR = None  # type: ignore


class WhisperService:
    """Provide speech recognition locally with safe fallbacks."""

    def __init__(self, model_size: str = "small", cache_dir: Path | str = "./models/stt") -> None:
        self.model_size = model_size
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._whisper_model = None
        self._speechbrain_model: Optional[EncoderDecoderASR] = None
        self._bootstrap_models()

    # ------------------------------------------------------------------
    def transcribe(self, audio_path: Path | str) -> str:
        """Transcribe audio from disk, falling back gracefully."""

        audio_path = Path(audio_path)

        if self._whisper_model is not None:
            try:  # pragma: no cover - heavy dependency
                result = self._whisper_model.transcribe(str(audio_path))
                return str(result.get("text", "")).strip()
            except Exception:
                pass

        if self._speechbrain_model is not None:
            try:  # pragma: no cover - heavy dependency
                return str(self._speechbrain_model.transcribe_file(str(audio_path))).strip()
            except Exception:
                pass

        return ""

    def status(self) -> dict:
        """Expose backend readiness for diagnostics."""

        return {
            "whisper_available": self._whisper_model is not None,
            "speechbrain_available": self._speechbrain_model is not None,
        }

    # ------------------------------------------------------------------
    def _bootstrap_models(self) -> None:
        if whisper is not None:
            try:  # pragma: no cover - heavy dependency
                self._whisper_model = whisper.load_model(self.model_size, download_root=str(self.cache_dir))
            except Exception:
                self._whisper_model = None

        if EncoderDecoderASR is not None:
            try:  # pragma: no cover - heavy dependency
                self._speechbrain_model = EncoderDecoderASR.from_hparams(
                    source="speechbrain/asr-transformer-transformerlm-librispeech",
                    savedir=str(self.cache_dir / "speechbrain"),
                )
            except Exception:
                self._speechbrain_model = None
