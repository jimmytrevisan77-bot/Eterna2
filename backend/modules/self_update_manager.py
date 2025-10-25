"""Self update and backup manager using GitPython when available."""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

try:  # pragma: no cover - optional dependency
    from git import Repo
except ImportError:  # pragma: no cover
    Repo = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from guardrails import Guard
except ImportError:  # pragma: no cover
    Guard = None  # type: ignore


class SelfUpdateManager:
    """Handle auto-backups and guarded patch application."""

    def __init__(self, project_root: Path | str = ".", backup_root: Path | str = "./Eterna/Backups") -> None:
        self.project_root = Path(project_root).resolve()
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.guard: Optional[Guard] = Guard() if Guard is not None else None

    def create_backup(self) -> Path:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
        destination = self.backup_root / timestamp
        destination.mkdir(parents=True, exist_ok=False)

        for entry in self.project_root.iterdir():
            if entry.name.startswith(".") or entry.name == "Eterna/Backups":
                continue
            target = destination / entry.name
            if entry.is_dir():
                shutil.copytree(entry, target)
            else:
                shutil.copy2(entry, target)

        archive_path = shutil.make_archive(str(destination), "zip", root_dir=destination)
        return Path(archive_path)

    def apply_patch(self, patch_commands: list[str]) -> bool:
        """Apply a list of shell commands representing a patch sequence."""

        backup = self.create_backup()
        try:
            for command in patch_commands:
                subprocess.check_call(command, shell=True)
            if Repo is not None:
                repo = Repo(self.project_root)
                repo.git.add(A=True)
                repo.index.commit(f"AUTO_PATCH_{datetime.utcnow():%Y%m%d_%H%M%S}")
            return True
        except subprocess.CalledProcessError:
            self._restore_backup(backup)
            return False

    def _restore_backup(self, archive_path: Path) -> None:
        restore_dir = archive_path.with_suffix("")
        if not restore_dir.exists():
            shutil.unpack_archive(str(archive_path), extract_dir=str(restore_dir))
        for entry in restore_dir.iterdir():
            target = self.project_root / entry.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if entry.is_dir():
                shutil.copytree(entry, target)
            else:
                shutil.copy2(entry, target)


__all__ = ["SelfUpdateManager"]
