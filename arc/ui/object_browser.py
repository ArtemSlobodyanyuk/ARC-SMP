from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QInputDialog,
    QMenu,
    QPushButton,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from arc.items.base_item import BaseItem


@dataclass(frozen=True)
class ShapeDef:
    key: str
    label: str


class ObjectBrowserDock(QDockWidget):
    """
    Simple object list with folder grouping.

    - Folders are purely organizational (stored as BaseItem.group string).
    - Selecting an item selects it in the scene.
    - Creating a shape places it into the selected folder (if any).
    """

    def __init__(
        self,
        *,
        create_object: Callable[[str, str], BaseItem | None],
        iter_items: Callable[[], list[BaseItem]],
        on_select_item: Callable[[BaseItem], None],
        shapes: Callable[[], list[ShapeDef]],
    ):
        super().__init__("Objects")

        self._create_object = create_object
        self._iter_items = iter_items
        self._on_select_item = on_select_item
        self._shapes = shapes
        self._suppress_selection = False

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self.add_button = QToolButton()
        self.add_button.setText("Add")
        self.add_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.add_menu = QMenu(self.add_button)
        self._rebuild_add_menu()
        self.add_button.setMenu(self.add_menu)

        self.new_folder_btn = QPushButton("New folder…")
        self.new_folder_btn.clicked.connect(self._new_folder)

        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.new_folder_btn)
        toolbar.addStretch(1)
        layout.addLayout(toolbar)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemSelectionChanged.connect(self._on_tree_selection_changed)
        layout.addWidget(self.tree)

        self.setWidget(root)

        self._folder_nodes: dict[str, QTreeWidgetItem] = {}
        self._item_nodes: dict[int, QTreeWidgetItem] = {}

        self.rebuild()

    def _rebuild_add_menu(self) -> None:
        self.add_menu.clear()
        for shape in self._shapes():
            self.add_menu.addAction(shape.label, lambda k=shape.key: self._add_shape(k))

    def refresh_shapes(self) -> None:
        self._rebuild_add_menu()

    def selected_folder(self) -> str:
        item = self.tree.currentItem()
        if item is None:
            return ""
        is_folder = bool(item.data(0, Qt.ItemDataRole.UserRole + 1))
        if is_folder:
            return str(item.data(0, Qt.ItemDataRole.UserRole))
        parent = item.parent()
        if parent is not None and bool(parent.data(0, Qt.ItemDataRole.UserRole + 1)):
            return str(parent.data(0, Qt.ItemDataRole.UserRole))
        return ""

    def rebuild(self) -> None:
        self._folder_nodes.clear()
        self._item_nodes.clear()

        self.tree.clear()
        root = QTreeWidgetItem(["Scene"])
        root.setExpanded(True)
        root.setData(0, Qt.ItemDataRole.UserRole, "")
        root.setData(0, Qt.ItemDataRole.UserRole + 1, True)  # is_folder
        self.tree.addTopLevelItem(root)
        self._folder_nodes[""] = root

        for obj in self._iter_items():
            self._ensure_folder(obj.group)
            self._add_item_node(obj)

        self.tree.expandAll()

    def ensure_folder_ui(self, group: str) -> None:
        self._ensure_folder(group)

    def sync_selection_from_scene(self, selected: list[BaseItem]) -> None:
        if self._suppress_selection:
            return
        self._suppress_selection = True
        try:
            self.tree.clearSelection()
            if not selected:
                return
            obj = selected[0]
            node = self._item_nodes.get(id(obj))
            if node is not None:
                self.tree.setCurrentItem(node)
        finally:
            self._suppress_selection = False

    def update_item_label(self, obj: BaseItem) -> None:
        node = self._item_nodes.get(id(obj))
        if node is not None:
            node.setText(0, obj.name)

    def _ensure_folder(self, group: str) -> QTreeWidgetItem:
        group = group or ""
        if group in self._folder_nodes:
            return self._folder_nodes[group]

        parent_group = ""
        name = group
        if "/" in group:
            parent_group, name = group.rsplit("/", 1)
        parent = self._ensure_folder(parent_group)

        node = QTreeWidgetItem([name])
        node.setData(0, Qt.ItemDataRole.UserRole, group)
        node.setData(0, Qt.ItemDataRole.UserRole + 1, True)  # is_folder
        parent.addChild(node)
        node.setExpanded(True)

        self._folder_nodes[group] = node
        return node

    def _add_item_node(self, obj: BaseItem) -> None:
        parent = self._folder_nodes.get(obj.group, self._folder_nodes[""])
        node = QTreeWidgetItem([obj.name])
        node.setData(0, Qt.ItemDataRole.UserRole, id(obj))
        node.setData(0, Qt.ItemDataRole.UserRole + 1, False)  # is_folder
        parent.addChild(node)
        self._item_nodes[id(obj)] = node

    def _new_folder(self) -> None:
        base = self.selected_folder()
        name, ok = QInputDialog.getText(self, "New folder", "Folder name:")
        if not ok:
            return
        name = (name or "").strip()
        if not name:
            return
        group = f"{base}/{name}" if base else name
        self._ensure_folder(group)
        self.tree.expandAll()

    def _add_shape(self, shape_key: str) -> None:
        group = self.selected_folder()
        obj = self._create_object(shape_key, group)
        if obj is None:
            return
        self.rebuild()

    def _on_tree_selection_changed(self) -> None:
        if self._suppress_selection:
            return
        item = self.tree.currentItem()
        if item is None:
            return
        is_folder = bool(item.data(0, Qt.ItemDataRole.UserRole + 1))
        if is_folder:
            return
        obj_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not isinstance(obj_id, int):
            return

        for obj in self._iter_items():
            if id(obj) == obj_id:
                self._suppress_selection = True
                try:
                    self._on_select_item(obj)
                finally:
                    self._suppress_selection = False
                return
