from PyQt6.QtWidgets import QGraphicsItem
from arc.ui.property_dialog import PropertyDialog


class BaseItem:

    def init_object(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.name = "object"
        self.note = ""

    def mouseDoubleClickEvent(self, event):
        dialog = PropertyDialog(self)
        dialog.exec()

    def resize(self, w, h):
        rect = self.rect()
        self.setRect(rect.x(), rect.y(), w, h)

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
