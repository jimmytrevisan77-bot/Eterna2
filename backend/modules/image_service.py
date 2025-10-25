"""Image enhancement utilities for local creative workflows."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional

from backend.eterna_core_manager import LifecycleModule

try:
    from realesrgan import RealESRGANer
except ModuleNotFoundError:  # pragma: no cover
    RealESRGANer = None  # type: ignore

try:
    from rembg import remove
except ModuleNotFoundError:  # pragma: no cover
    remove = None  # type: ignore


class ImageService(LifecycleModule):
    """Handles upscaling and background removal locally."""

    name = "image_service"

    def __init__(self, model_path: Optional[Path] = None, output_dir: Optional[Path] = None) -> None:
        self._model_path = model_path or Path("models") / "realesrgan" / "RealESRGAN_x4plus.pth"
        self._output_dir = output_dir or Path("outputs") / "images"
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._upscaler: Optional[RealESRGANer] = None  # type: ignore[assignment]
        self._logger = logging.getLogger("ImageService")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def start(self) -> None:
        if RealESRGANer is None:
            self._logger.warning("Real-ESRGAN not installed; upscaling disabled")
            return
        try:
            self._upscaler = RealESRGANer(
                model_path=str(self._model_path),
                model=None,
                netscale=4,
            )
            self._logger.info("Real-ESRGAN model ready")
        except Exception as exc:  # pragma: no cover - external
            self._logger.warning("Failed to load Real-ESRGAN model: %s", exc)

    def stop(self) -> None:
        self._upscaler = None

    def status(self) -> Dict[str, Optional[bool]]:
        return {
            "upscaler": self._upscaler is not None,
            "background_removal": remove is not None,
        }

    def upscale(self, image_path: Path) -> Path:
        if self._upscaler is None:
            raise RuntimeError("Real-ESRGAN model is not initialised")
        output = self._output_dir / f"{image_path.stem}_x4.png"
        image = self._upscaler.enhance(str(image_path))[0]
        image.save(output)
        self._logger.info("Upscaled %s -> %s", image_path, output)
        return output

    def remove_background(self, image_path: Path) -> Path:
        if remove is None:
            raise RuntimeError("rembg is required for background removal")
        with image_path.open("rb") as src:
            data = src.read()
        result = remove(data)
        output = self._output_dir / f"{image_path.stem}_nobg.png"
        with output.open("wb") as handle:
            handle.write(result)
        self._logger.info("Removed background from %s", image_path)
        return output


__all__ = ["ImageService"]
