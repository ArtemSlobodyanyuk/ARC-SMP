from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QToolBar,
    QMenu,
    QToolButton,
    QFileDialog,
    QMessageBox,
)

import json
from pathlib import Path

from arc.core.factory import ObjectFactory
from arc.items.base_item import BaseItem


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARC prototype")
        self.resize(900, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.factory = ObjectFactory(self.scene)
        self.saves_dir = Path(__file__).resolve().parents[2] / "saves"
        self.saves_dir.mkdir(parents=True, exist_ok=True)

        self.init_toolbar()

    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.addAction("Save", self.save_scene)
        toolbar.addAction("Load", self.load_scene)

        add_button = QToolButton()
        add_button.setText("Add items")
        add_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        menu = QMenu()

        menu.addAction("Circle", lambda: self.factory.create("circle"))
        menu.addAction("Square", lambda: self.factory.create("square"))
        menu.addAction("Rectangle", lambda: self.factory.create("rectangle"))

        add_button.setMenu(menu)
        toolbar.addWidget(add_button)

    def _serialize_scene(self) -> list[dict]:
        # QGraphicsScene.items() returns items in stacking order; order isn't important for now.
        data: list[dict] = []
        for item in self.scene.items():
            if isinstance(item, BaseItem):
                data.append(item.to_dict())
        return data

    def save_scene(self):
        default_path = str(self.saves_dir / "scene.json")
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save scene",
            default_path,
            "JSON (*.json)",
        )
        if not filename:
            return

        try:
            payload = {"version": 1, "items": self._serialize_scene()}
            Path(filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))

    def load_scene(self):
        default_path = str(self.saves_dir)
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load scene",
            default_path,
            "JSON (*.json)",
        )
        if not filename:
            return

        try:
            payload = json.loads(Path(filename).read_text(encoding="utf-8"))
            items = payload.get("items", [])
        except Exception as e:
            QMessageBox.critical(self, "Load failed", str(e))
            return

        self.scene.clear()
        for item_data in items:
            if isinstance(item_data, dict):
                self.factory.create_from_data(item_data)
