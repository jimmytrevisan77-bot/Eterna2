"""Core backend package for the Eterna autonomous desktop stack."""

from .eterna_core_manager import EternaCoreManager
from .ios_bridge import IOSBridge
from . import modules

__all__ = [
    "EternaCoreManager",
    "IOSBridge",
    "modules",
]
