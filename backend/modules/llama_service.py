"""Local LLaMA/Mistral text generation helper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:  # pragma: no cover - optional dependency
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
except Exception:  # pragma: no cover - degrade gracefully without transformers
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    pipeline = None  # type: ignore


@dataclass
class GenerationConfig:
    model_name: str = "meta-llama/Llama-3-8b"
    max_new_tokens: int = 256
    temperature: float = 0.7
    device: str | int | None = "cuda" if AutoModelForCausalLM else None


class LlamaService:
    """Lightweight wrapper around a local LLaMA compatible model."""

    def __init__(self, cache_dir: Path | str = "./models/llm", config: Optional[GenerationConfig] = None) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or GenerationConfig()
        self._generator = None
        self._bootstrap_model()

    # ------------------------------------------------------------------
    def generate(self, prompt: str) -> str:
        """Generate a completion for the supplied prompt."""

        if self._generator is None:
            return "[Text generation unavailable – install transformers + compatible weights]"

        result = self._generator(
            prompt,
            max_new_tokens=self.config.max_new_tokens,
            temperature=self.config.temperature,
            do_sample=True,
        )
        if isinstance(result, list):
            return result[0]["generated_text"]
        return str(result)

    def status(self) -> dict:
        """Expose readiness state for diagnostics."""

        return {"generator_ready": self._generator is not None}

    # ------------------------------------------------------------------
    def _bootstrap_model(self) -> None:
        if pipeline is None or AutoTokenizer is None or AutoModelForCausalLM is None:
            return

        try:  # pragma: no cover - heavy dependency
            self._generator = pipeline(
                "text-generation",
                model=self.config.model_name,
                tokenizer=self.config.model_name,
                model_kwargs={"torch_dtype": "auto"},
                device=self.config.device,
                cache_dir=str(self.cache_dir),
            )
        except Exception:
            self._generator = None
