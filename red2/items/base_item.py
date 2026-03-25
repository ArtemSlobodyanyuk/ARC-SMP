from PyQt6.QtWidgets import QGraphicsItem
from red2.ui.property_dialog import PropertyDialog


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