from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QCursor, QPen
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem

from arc.ui.property_dialog import PropertyDialog


HandlePos = Literal["n", "s", "e", "w", "ne", "nw", "se", "sw"]


@dataclass(frozen=True)
class _ResizeState:
    handle: HandlePos
    start_scene_pos: QPointF
    start_rect: QRectF


class _ResizeHandle(QGraphicsRectItem):
    def __init__(self, parent: "BaseItem", pos: HandlePos, size: float = 8.0):
        super().__init__(-size / 2.0, -size / 2.0, size, size, parent)
        self._parent = parent
        self._pos: HandlePos = pos

        self.setBrush(QColor("#ffffff"))
        self.setPen(QPen(QColor("#1f2937"), 1.0))
        self.setZValue(10_000)
        self.setVisible(False)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.setAcceptHoverEvents(True)

    @property
    def pos_key(self) -> HandlePos:
        return self._pos

    def hoverEnterEvent(self, event):
        cursor = Qt.CursorShape.ArrowCursor
        if self._pos in ("n", "s"):
            cursor = Qt.CursorShape.SizeVerCursor
        elif self._pos in ("e", "w"):
            cursor = Qt.CursorShape.SizeHorCursor
        elif self._pos in ("ne", "sw"):
            cursor = Qt.CursorShape.SizeBDiagCursor
        elif self._pos in ("nw", "se"):
            cursor = Qt.CursorShape.SizeFDiagCursor
        self.setCursor(QCursor(cursor))
        super().hoverEnterEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._parent._begin_resize(self._pos, event.scenePos())
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self._parent._update_resize(event.scenePos())
        event.accept()

    def mouseReleaseEvent(self, event):
        self._parent._end_resize()
        event.accept()


class BaseItem:

    def init_object(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.name = "object"
        self.note = ""

        self._resize_state: _ResizeState | None = None
        self._handles: dict[HandlePos, _ResizeHandle] = {}
        self._init_resize_handles()

    def mouseDoubleClickEvent(self, event):
        dialog = PropertyDialog(self)
        dialog.exec()

    def resize(self, w, h):
        rect = self.rect()
        self.setRect(rect.x(), rect.y(), w, h)
        self._sync_handles()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            selected = bool(value)
            for handle in self._handles.values():
                handle.setVisible(selected)
            if selected:
                self._sync_handles()
        return super().itemChange(change, value)

    def _init_resize_handles(self):
        for pos in ("n", "s", "e", "w", "ne", "nw", "se", "sw"):
            self._handles[pos] = _ResizeHandle(self, pos)
        self._sync_handles()

    def _sync_handles(self):
        if not self._handles:
            return
        rect = self.rect()
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        cx = rect.center().x()
        cy = rect.center().y()

        positions: dict[HandlePos, QPointF] = {
            "n": QPointF(cx, top),
            "s": QPointF(cx, bottom),
            "w": QPointF(left, cy),
            "e": QPointF(right, cy),
            "nw": QPointF(left, top),
            "ne": QPointF(right, top),
            "sw": QPointF(left, bottom),
            "se": QPointF(right, bottom),
        }
        for key, handle in self._handles.items():
            handle.setPos(positions[key])

    def _begin_resize(self, handle: HandlePos, scene_pos: QPointF):
        self._resize_state = _ResizeState(
            handle=handle,
            start_scene_pos=scene_pos,
            start_rect=QRectF(self.rect()),
        )

    def _update_resize(self, scene_pos: QPointF):
        if self._resize_state is None:
            return
        state = self._resize_state

        start_local = self.mapFromScene(state.start_scene_pos)
        cur_local = self.mapFromScene(scene_pos)
        delta = cur_local - start_local

        rect = QRectF(state.start_rect)
        min_size = 16.0

        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()

        if state.handle in ("w", "nw", "sw"):
            left = left + delta.x()
        if state.handle in ("e", "ne", "se"):
            right = right + delta.x()
        if state.handle in ("n", "nw", "ne"):
            top = top + delta.y()
        if state.handle in ("s", "sw", "se"):
            bottom = bottom + delta.y()

        # Clamp to minimum size
        if (right - left) < min_size:
            if state.handle in ("w", "nw", "sw"):
                left = right - min_size
            else:
                right = left + min_size
        if (bottom - top) < min_size:
            if state.handle in ("n", "nw", "ne"):
                top = bottom - min_size
            else:
                bottom = top + min_size

        new_rect = QRectF(QPointF(left, top), QPointF(right, bottom))
        self.setRect(new_rect)
        self._sync_handles()

    def _end_resize(self):
        self._resize_state = None

    def to_dict(self) -> dict:
        rect = self.rect()
        pos = self.pos()
        return {
            "type": getattr(self, "item_type", "unknown"),
            "x": float(pos.x()),
            "y": float(pos.y()),
            "w": float(rect.width()),
            "h": float(rect.height()),
            "name": getattr(self, "name", "object"),
            "note": getattr(self, "note", ""),
        }
