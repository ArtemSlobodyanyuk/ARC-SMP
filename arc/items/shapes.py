from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import QRectF

from arc.items.base_item import BaseItem


class CircleItem(BaseItem, QGraphicsEllipseItem):

    def __init__(self):
        QGraphicsEllipseItem.__init__(self, QRectF(0, 0, 80, 80))
        self.setBrush(QBrush(QColor("#3498db")))
        self.item_type = "circle"
        self.init_object()


class SquareItem(BaseItem, QGraphicsRectItem):

    def __init__(self):
        QGraphicsRectItem.__init__(self, QRectF(0, 0, 80, 80))
        self.setBrush(QBrush(QColor("#2ecc71")))
        self.item_type = "square"
        self.init_object()


class RectangleItem(BaseItem, QGraphicsRectItem):

    def __init__(self):
        QGraphicsRectItem.__init__(self, QRectF(0, 0, 120, 70))
        self.setBrush(QBrush(QColor("#e67e22")))
        self.item_type = "rectangle"
        self.init_object()
