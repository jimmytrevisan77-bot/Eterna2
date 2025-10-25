"""Adaptive security utilities for biometric and OTP flows."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Optional

try:  # pragma: no cover - optional dependency
    from speechbrain.pretrained import SpeakerRecognition
except ImportError:  # pragma: no cover
    SpeakerRecognition = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import face_recognition
except ImportError:  # pragma: no cover
    face_recognition = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import pyotp
except ImportError:  # pragma: no cover
    pyotp = None  # type: ignore


@dataclass
class SecurityStatus:
    voice_ready: bool
    face_ready: bool
    otp_ready: bool


class SecurityManager:
    """Coordinate biometric verifications and OTP challenges."""

    def __init__(self) -> None:
        self._speaker_recognition = None
        if SpeakerRecognition is not None:  # pragma: no cover
            try:
                self._speaker_recognition = SpeakerRecognition.from_hparams(
                    source="speechbrain/spkrec-ecapa-voxceleb"
                )
            except Exception:
                self._speaker_recognition = None
        self._otp_secret = pyotp.random_base32() if pyotp is not None else secrets.token_hex(16)

    def verify_voice(self, sample_a: str, sample_b: str) -> Optional[float]:
        if self._speaker_recognition is None:  # pragma: no cover
            return None
        try:  # pragma: no cover - requires models
            score, prediction = self._speaker_recognition.verify_files(sample_a, sample_b)
            return float(score)
        except Exception:
            return None

    def verify_face(self, image_a: str, image_b: str) -> Optional[float]:
        if face_recognition is None:  # pragma: no cover
            return None
        try:  # pragma: no cover - heavy dependency
            encoding_a = face_recognition.face_encodings(face_recognition.load_image_file(image_a))[0]
            encoding_b = face_recognition.face_encodings(face_recognition.load_image_file(image_b))[0]
            distance = face_recognition.face_distance([encoding_a], encoding_b)[0]
            return float(1 - distance)
        except Exception:
            return None

    def current_otp(self) -> Optional[str]:
        if pyotp is None:  # pragma: no cover
            return None
        totp = pyotp.TOTP(self._otp_secret)
        return totp.now()

    def status(self) -> SecurityStatus:
        return SecurityStatus(
            voice_ready=self._speaker_recognition is not None,
            face_ready=face_recognition is not None,
            otp_ready=pyotp is not None,
        )


__all__ = ["SecurityManager", "SecurityStatus"]
