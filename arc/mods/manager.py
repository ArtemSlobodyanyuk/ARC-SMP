from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from PyQt6.QtCore import QStandardPaths


@dataclass(frozen=True)
class ModInfo:
    mod_id: str
    name: str
    version: str
    path: Path
    entrypoint: str


class ModAPI:
    def __init__(self, *, main_window, factory):
        self.main_window = main_window
        self.factory = factory

    def register_shape(self, key: str, ctor: Callable[[], Any], *, label: str | None = None) -> None:
        self.factory.register(key, ctor, label=label)


class ModManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.mods_root = repo_root / "mods"
        self.mods_root.mkdir(parents=True, exist_ok=True)

        self._enabled_path = self._config_dir() / "enabled_mods.json"
        self._enabled_path.parent.mkdir(parents=True, exist_ok=True)

    def _config_dir(self) -> Path:
        base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        if not base:
            return Path.home() / ".arc_platform"
        return Path(base)

    def list_mods(self) -> list[ModInfo]:
        mods: list[ModInfo] = []
        if not self.mods_root.exists():
            return mods

        for child in sorted(self.mods_root.iterdir(), key=lambda p: p.name.lower()):
            if not child.is_dir():
                continue

            manifest = child / "mod.json"
            if manifest.exists():
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                except Exception:
                    continue
                mod_id = str(data.get("id") or child.name)
                name = str(data.get("name") or mod_id)
                version = str(data.get("version") or "0.0.0")
                entrypoint = str(data.get("entrypoint") or "mod:register")
            else:
                mod_id = child.name
                name = mod_id
                version = "0.0.0"
                entrypoint = "mod:register"

            mods.append(ModInfo(mod_id=mod_id, name=name, version=version, path=child, entrypoint=entrypoint))

        return mods

    def enabled_ids(self) -> set[str]:
        try:
            data = json.loads(self._enabled_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return {str(x) for x in data}
        except Exception:
            pass
        return set()

    def set_enabled_ids(self, ids: set[str]) -> None:
        self._enabled_path.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8")

    def apply_enabled(self, *, main_window, factory) -> list[str]:
        applied: list[str] = []
        enabled = self.enabled_ids()
        mods = self.list_mods()
        if not mods:
            return applied

        # Allow importing `mods/<mod>` by adding mods_root to sys.path.
        mods_path_str = str(self.mods_root)
        added = False
        if mods_path_str not in sys.path:
            sys.path.insert(0, mods_path_str)
            added = True

        try:
            api = ModAPI(main_window=main_window, factory=factory)
            for info in mods:
                if info.mod_id not in enabled:
                    continue
                if self._apply_one(info, api):
                    applied.append(info.mod_id)
        finally:
            if added:
                try:
                    sys.path.remove(mods_path_str)
                except ValueError:
                    pass

        return applied

    def _apply_one(self, info: ModInfo, api: ModAPI) -> bool:
        # entrypoint format: "module.sub:func"
        mod_part, _, func_part = info.entrypoint.partition(":")
        module_name = mod_part.strip() or "mod"
        func_name = (func_part.strip() or "register")

        try:
            module = import_module(f"{info.path.name}.{module_name}")
        except Exception:
            # fallback: allow "<module>" directly if mod is a package on sys.path
            try:
                module = import_module(module_name)
            except Exception:
                return False

        func = getattr(module, func_name, None)
        if not callable(func):
            return False

        try:
            func(api)
            return True
        except Exception:
            return False

