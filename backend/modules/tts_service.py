"""Local text-to-speech helper leveraging Coqui TTS when available."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:  # pragma: no cover - optional dependency
    from TTS.api import TTS
except Exception:  # pragma: no cover - degrade gracefully
    TTS = None  # type: ignore


class TTSService:
    """Generate speech locally and expose audio file handles to the UI."""

    def __init__(self, model_name: str = "tts_models/en/vctk/vits", output_root: Path | str = "./output/tts") -> None:
        self.model_name = model_name
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)
        self._engine: Optional[TTS] = None
        self._bootstrap_engine()

    # ------------------------------------------------------------------
    def synthesize(self, text: str, speaker: Optional[str] = None) -> Path:
        """Synthesize an utterance and return the audio path."""

        target_file = self.output_root / "last_tts.wav"

        if self._engine is None:
            target_file.write_bytes(b"")
            return target_file

        kwargs = {"file_path": str(target_file)}
        if speaker:
            kwargs["speaker"] = speaker

        try:  # pragma: no cover - heavy dependency
            self._engine.tts_to_file(text=text, **kwargs)
        except Exception:
            target_file.write_bytes(b"")

        return target_file

    def status(self) -> dict:
        """Return whether the TTS backend is ready."""

        return {"engine_ready": self._engine is not None, "output_directory": str(self.output_root)}

    # ------------------------------------------------------------------
    def _bootstrap_engine(self) -> None:
        if TTS is None:
            return

        try:  # pragma: no cover - heavy dependency
            self._engine = TTS(model_name=self.model_name, progress_bar=False)
        except Exception:
            self._engine = None
