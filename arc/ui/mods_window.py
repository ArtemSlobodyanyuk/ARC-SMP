from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt

from arc.mods.manager import ModManager


class ModsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mods")
        self.resize(520, 420)

        self.repo_root = Path(__file__).resolve().parents[2]
        self.manager = ModManager(self.repo_root)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Увімкніть моди (після зміни відкрийте редактор заново)."))

        self.list = QListWidget()
        layout.addWidget(self.list)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self._load()

    def _load(self) -> None:
        enabled = self.manager.enabled_ids()
        self.list.clear()
        for mod in self.manager.list_mods():
            item = QListWidgetItem(f"{mod.name}  ({mod.mod_id})  v{mod.version}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if mod.mod_id in enabled else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, mod.mod_id)
            self.list.addItem(item)

    def _save(self) -> None:
        enabled: set[str] = set()
        for i in range(self.list.count()):
            item = self.list.item(i)
            mod_id = item.data(Qt.ItemDataRole.UserRole)
            if item.checkState() == Qt.CheckState.Checked and isinstance(mod_id, str):
                enabled.add(mod_id)
        self.manager.set_enabled_ids(enabled)
        self.accept()

