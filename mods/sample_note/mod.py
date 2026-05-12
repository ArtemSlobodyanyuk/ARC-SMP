from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsRectItem

from arc.items.base_item import BaseItem


class NoteStickerItem(BaseItem, QGraphicsRectItem):
    def __init__(self):
        QGraphicsRectItem.__init__(self, QRectF(0, 0, 160, 120))
        self.setBrush(QBrush(QColor("#fff3b0")))
        self.item_type = "note_sticker"
        self.init_object()


def register(api) -> None:
    # Adds a new shape to the "Add" menu + factory.
    api.register_shape("note_sticker", NoteStickerItem, label="Note Sticker")

