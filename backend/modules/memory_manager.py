"""Hybrid local memory manager for Eterna.

The manager favours ChromaDB for vector lookups when available, then TinyDB
as a lightweight JSON store. A pure in-memory fallback keeps the module
operational on pristine environments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

try:  # pragma: no cover - optional dependency
    import chromadb
    from chromadb.api.models.Collection import Collection
except ImportError:  # pragma: no cover - environment fallback
    chromadb = None
    Collection = object  # type: ignore

try:  # pragma: no cover - optional dependency
    from tinydb import Query, TinyDB
except ImportError:  # pragma: no cover - environment fallback
    TinyDB = None  # type: ignore
    Query = None  # type: ignore


Scope = str


@dataclass
class MemoryRecord:
    """Single memory entry tracked by the manager."""

    scope: Scope
    text: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    metadata: Optional[dict] = None


class EternaMemoryManager:
    """Manage professional and personal long-term memories."""

    PROFESSIONAL_SCOPE = "professional"
    PERSONAL_SCOPE = "personal"

    def __init__(self, storage_root: Path | str = "./storage/memory") -> None:
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

        self._chroma_client = None
        self._personal_collection: Optional[Collection] = None
        self._professional_collection: Optional[Collection] = None
        self._tinydb: Optional[TinyDB] = None
        self._fallback_store: Dict[Scope, List[MemoryRecord]] = {
            self.PROFESSIONAL_SCOPE: [],
            self.PERSONAL_SCOPE: [],
        }

        self._bootstrap_backends()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def store_memory(
        self,
        text: str,
        scope: Scope,
        tags: Optional[Iterable[str]] = None,
        metadata: Optional[dict] = None,
    ) -> MemoryRecord:
        """Persist a new memory in the configured storage layer."""

        record = MemoryRecord(scope=scope, text=text, tags=list(tags or []), metadata=metadata)

        if self._personal_collection and self._professional_collection:
            collection = (
                self._professional_collection if scope == self.PROFESSIONAL_SCOPE else self._personal_collection
            )
            collection.add(
                documents=[record.text],
                metadatas=[{
                    "created_at": record.created_at.isoformat(),
                    "tags": record.tags,
                    "scope": record.scope,
                    **(record.metadata or {}),
                }],
                ids=[f"{record.scope}-{record.created_at.timestamp()}"],
            )
        elif self._tinydb:
            self._tinydb.insert(
                {
                    "scope": record.scope,
                    "text": record.text,
                    "created_at": record.created_at.isoformat(),
                    "tags": record.tags,
                    "metadata": record.metadata or {},
                }
            )
        else:
            self._fallback_store.setdefault(scope, []).append(record)

        return record

    def fetch_scope(self, scope: Scope) -> List[MemoryRecord]:
        """Return memories for a specific scope."""

        if self._tinydb:
            assert Query is not None  # for type checkers
            scoped = self._tinydb.search(Query().scope == scope)
            return [
                MemoryRecord(
                    scope=item["scope"],
                    text=item["text"],
                    created_at=datetime.fromisoformat(item["created_at"]),
                    tags=item.get("tags", []),
                    metadata=item.get("metadata"),
                )
                for item in scoped
            ]

        if scope not in self._fallback_store:
            return []

        return list(self._fallback_store[scope])

    def similarity_search(self, scope: Scope, query: str, top_k: int = 3) -> List[str]:
        """Perform a simple similarity lookup using ChromaDB when available."""

        if self._personal_collection and self._professional_collection:
            collection = (
                self._professional_collection if scope == self.PROFESSIONAL_SCOPE else self._personal_collection
            )
            results = collection.query(query_texts=[query], n_results=top_k)
            documents = results.get("documents", [[]])[0]
            return [str(doc) for doc in documents]

        # fallback: naive substring search
        return [
            record.text
            for record in self._fallback_store.get(scope, [])
            if query.lower() in record.text.lower()
        ][:top_k]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _bootstrap_backends(self) -> None:
        if chromadb is not None:  # pragma: no cover - optional branch
            try:
                self._chroma_client = chromadb.PersistentClient(path=str(self.storage_root / "chroma"))
                self._professional_collection = self._chroma_client.get_or_create_collection("eterna_pro")
                self._personal_collection = self._chroma_client.get_or_create_collection("eterna_personal")
                return
            except Exception:  # pragma: no cover - degrade gracefully
                self._chroma_client = None

        if TinyDB is not None:
            tiny_path = self.storage_root / "memory.json"
            self._tinydb = TinyDB(tiny_path)
            return

        # fallback store is already initialised
        return


__all__ = ["EternaMemoryManager", "MemoryRecord"]
