"""Local text generation service built around Hugging Face transformers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from backend.eterna_core_manager import LifecycleModule

try:  # Optional heavy dependency
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
except ModuleNotFoundError:  # pragma: no cover
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    torch = None  # type: ignore


class LlamaService(LifecycleModule):
    """Loads a local LLaMA-compatible model for fully offline inference."""

    name = "llama_service"

    def __init__(self, model_name: str = "meta-llama/Llama-3-8b", device: Optional[str] = None, cache_dir: Optional[Path] = None) -> None:
        self._model_name = model_name
        self._device = device or ("cuda" if torch and torch.cuda.is_available() else "cpu")
        self._cache_dir = cache_dir
        self._model: Optional[Any] = None
        self._tokenizer: Optional[Any] = None
        self._logger = logging.getLogger("LlamaService")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def start(self) -> None:
        if AutoModelForCausalLM is None or AutoTokenizer is None:
            self._logger.warning("transformers not installed; skipping LLaMA initialisation")
            return
        self._logger.info("Loading model %s on %s", self._model_name, self._device)
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name, cache_dir=self._cache_dir)
        self._model = AutoModelForCausalLM.from_pretrained(self._model_name, device_map=self._device, cache_dir=self._cache_dir)

    def stop(self) -> None:
        self._model = None
        self._tokenizer = None

    def status(self) -> Dict[str, Any]:
        return {
            "model_name": self._model_name,
            "device": self._device,
            "loaded": self._model is not None,
        }

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("Model is not loaded")
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._device)
        with torch.no_grad():  # type: ignore[operator]
            outputs = self._model.generate(**inputs, max_new_tokens=max_tokens)
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)


__all__ = ["LlamaService"]
