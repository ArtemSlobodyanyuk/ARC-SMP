from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QToolBar,
    QMenu,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt

import json
from pathlib import Path

from arc.core.factory import ObjectFactory
from arc.items.base_item import BaseItem
from arc.ui.object_browser import ObjectBrowserDock
from arc.mods.manager import ModManager


class CanvasView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setInteractive(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        scene_pos = self.mapToScene(event.pos())
        item = self.scene().itemAt(scene_pos, self.transform())

        if isinstance(item, BaseItem):
            scene = item.scene()
            if scene is not None:
                scene.clearSelection()
            item.setSelected(True)

        delete_action = menu.addAction("Delete")
        delete_action.setEnabled(isinstance(item, BaseItem))

        chosen_action = menu.exec(event.globalPos())
        if chosen_action is delete_action and isinstance(item, BaseItem):
            scene = item.scene()
            if scene is not None:
                scene.removeItem(item)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARC prototype")
        self.resize(900, 600)

        self.scene = QGraphicsScene()
        self.view = CanvasView(self.scene)
        self.setCentralWidget(self.view)

        self.factory = ObjectFactory(self.scene)
        self.saves_dir = Path(__file__).resolve().parents[2] / "saves"
        self.saves_dir.mkdir(parents=True, exist_ok=True)

        self.mod_manager = ModManager(Path(__file__).resolve().parents[2])

        self.object_browser = ObjectBrowserDock(
            create_object=self._create_object,
            iter_items=self._iter_items,
            on_select_item=self._select_item_in_scene,
            shapes=self._shape_defs,
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.object_browser)

        self.scene.selectionChanged.connect(self._on_scene_selection_changed)

        self.init_toolbar()

        # Apply enabled mods (may register extra shapes, actions, etc.)
        self.mod_manager.apply_enabled(main_window=self, factory=self.factory)
        self.object_browser.refresh_shapes()

    def load_scene_from_file(self, filename: str) -> None:
        try:
            payload = json.loads(Path(filename).read_text(encoding="utf-8"))
            items = payload.get("items", [])
        except Exception as e:
            QMessageBox.critical(self, "Load failed", str(e))
            return

        self.scene.clear()
        for item_data in items:
            if isinstance(item_data, dict):
                obj = self.factory.create_from_data(item_data)
                if isinstance(obj, BaseItem):
                    obj.set_on_properties_saved(self._on_item_saved)

        self.object_browser.rebuild()

    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.addAction("Save", self.save_scene)
        toolbar.addAction("Load", self.load_scene)

    def _iter_items(self) -> list[BaseItem]:
        items: list[BaseItem] = []
        for item in self.scene.items():
            if isinstance(item, BaseItem):
                items.append(item)
        return items

    def _shape_defs(self):
        from arc.ui.object_browser import ShapeDef

        return [ShapeDef(k, label) for k, label in self.factory.available()]

    def _create_object(self, obj_type: str, group: str) -> BaseItem | None:
        obj = self.factory.create(obj_type)
        if obj is None:
            return None
        obj.group = group or ""
        obj.set_on_properties_saved(self._on_item_saved)
        return obj

    def _select_item_in_scene(self, obj: BaseItem) -> None:
        self.scene.clearSelection()
        obj.setSelected(True)
        self.view.centerOn(obj)

    def _on_scene_selection_changed(self) -> None:
        selected = [i for i in self.scene.selectedItems() if isinstance(i, BaseItem)]
        self.object_browser.sync_selection_from_scene(selected)

    def _on_item_saved(self, obj: object) -> None:
        if isinstance(obj, BaseItem):
            self.object_browser.update_item_label(obj)

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

        self.load_scene_from_file(filename)
