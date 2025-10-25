"""Persistent memory store with professional/personal separation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

try:  # Optional dependency
    from tinydb import TinyDB
except ModuleNotFoundError:  # pragma: no cover - optional import guard
    TinyDB = None  # type: ignore

from backend.eterna_core_manager import LifecycleModule


class MemoryManager(LifecycleModule):
    """Provides lightweight long-term storage using TinyDB or JSON files."""

    name = "memory_manager"

    def __init__(self, root: Optional[Path] = None) -> None:
        self._root = root or Path("config") / "Memory"
        self._root.mkdir(parents=True, exist_ok=True)
        self._db_personal: Optional[TinyDB] = None  # type: ignore
        self._db_professional: Optional[TinyDB] = None  # type: ignore

    def start(self) -> None:
        if TinyDB is None:
            return
        self._db_personal = TinyDB(self._root / "personal.json")
        self._db_professional = TinyDB(self._root / "professional.json")

    def stop(self) -> None:
        if self._db_personal:
            self._db_personal.close()
        if self._db_professional:
            self._db_professional.close()

    def status(self) -> Dict[str, Any]:
        return {
            "backend": "tinydb" if TinyDB else "json",
            "personal_entries": self._count_entries(self._db_personal, self._root / "personal.json"),
            "professional_entries": self._count_entries(self._db_professional, self._root / "professional.json"),
        }

    def _count_entries(self, db: Optional[TinyDB], fallback_path: Path) -> int:
        if db:
            return len(db)
        if fallback_path.exists():
            with fallback_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return len(data)
        return 0

    def add_memory(self, category: str, payload: Dict[str, Any]) -> None:
        if category not in {"personal", "professional"}:
            raise ValueError("category must be 'personal' or 'professional'")
        if TinyDB is None:
            self._write_json(category, payload)
            return
        db = self._db_personal if category == "personal" else self._db_professional
        if db is None:
            self._write_json(category, payload)
        else:
            db.insert(payload)

    def _write_json(self, category: str, payload: Dict[str, Any]) -> None:
        target = self._root / f"{category}.json"
        existing = []
        if target.exists():
            with target.open("r", encoding="utf-8") as handle:
                existing = json.load(handle)
        existing.append(payload)
        with target.open("w", encoding="utf-8") as handle:
            json.dump(existing, handle, indent=2)


__all__ = ["MemoryManager"]
