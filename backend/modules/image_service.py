"""Image enhancement pipeline hooking Real-ESRGAN and RemBG when present."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

try:  # pragma: no cover - optional dependency
    from realesrgan import RealESRGANer
except ImportError:  # pragma: no cover
    RealESRGANer = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from rembg import remove as _rembg_remove
    _rembg_available = True
except ImportError:  # pragma: no cover
    _rembg_available = False

    def _rembg_remove(data: bytes) -> bytes:  # type: ignore
        return data

try:  # pragma: no cover - optional dependency
    import cv2  # type: ignore
except ImportError:  # pragma: no cover
    cv2 = None  # type: ignore


class ImageService:
    """Improve images with super resolution and background removal."""

    def __init__(self, models_path: Path | str = "./storage/models") -> None:
        self.models_path = Path(models_path)
        self.models_path.mkdir(parents=True, exist_ok=True)
        self._realesrgan: Optional[RealESRGANer] = None

        if RealESRGANer is not None:  # pragma: no cover - optional branch
            try:
                from basicsr.archs.rrdbnet_arch import RRDBNet  # type: ignore

                model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
                self._realesrgan = RealESRGANer(
                    model_path=str(self.models_path / "RealESRGAN_x4plus.pth"),
                    model=model,
                    half=True,
                )
            except Exception:
                self._realesrgan = None

    def upscale(self, image_path: Path | str, output_path: Path | str) -> Path:
        source = Path(image_path)
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)

        if self._realesrgan is None:  # pragma: no cover
            # fallback: copy file as-is
            destination.write_bytes(source.read_bytes())
            return destination

        try:  # pragma: no cover - heavy dependency
            enhanced = self._realesrgan.enhance(str(source))
            image_bytes = self._serialize_image(enhanced)
            if image_bytes is not None:
                destination.write_bytes(image_bytes)
            else:
                destination.write_bytes(source.read_bytes())
            return destination
        except Exception:
            destination.write_bytes(source.read_bytes())
            return destination

    def remove_background(self, image_bytes: bytes) -> bytes:
        return _rembg_remove(image_bytes)

    def _serialize_image(self, enhanced: Tuple) -> Optional[bytes]:
        if isinstance(enhanced, tuple):
            image = enhanced[0]
        else:
            image = enhanced
        if cv2 is None:  # pragma: no cover
            return None
        try:  # pragma: no cover
            success, buffer = cv2.imencode(".png", image)
            if success:
                return buffer.tobytes()
        except Exception:
            return None
        return None

    def status(self) -> dict:
        """Return diagnostic information for the image pipeline."""

        return {
            "realesrgan_available": self._realesrgan is not None,
            "rembg_available": _rembg_available,
            "opencv_available": cv2 is not None,
        }


__all__ = ["ImageService"]
