from __future__ import annotations

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QBrush, QColor, QPainter, QPolygonF, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem

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


class EllipseItem(BaseItem, QGraphicsEllipseItem):

    def __init__(self):
        QGraphicsEllipseItem.__init__(self, QRectF(0, 0, 140, 80))
        self.setBrush(QBrush(QColor("#8e44ad")))
        self.item_type = "ellipse"
        self.init_object()


class RoundedRectItem(BaseItem, QGraphicsRectItem):

    def __init__(self):
        QGraphicsRectItem.__init__(self, QRectF(0, 0, 140, 80))
        self.setBrush(QBrush(QColor("#16a085")))
        self.item_type = "rounded_rect"
        self.init_object()

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawRoundedRect(self.rect(), 14.0, 14.0)


class _PolygonInRectItem(BaseItem, QGraphicsRectItem):
    # A "rect item" that actually paints a polygon inside its rect,
    # so resizing/serialization continues to work via BaseItem.rect().

    item_type: str = "polygon"

    def __init__(self, rect: QRectF):
        QGraphicsRectItem.__init__(self, rect)
        self.setBrush(QBrush(QColor("#95a5a6")))
        # Hide the default rect outline; we paint everything ourselves.
        self.setPen(QPen(QColor("#1f2937"), 1.0))
        self.init_object()

    def _polygon(self) -> QPolygonF:
        raise NotImplementedError

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawPolygon(self._polygon())


class TriangleItem(_PolygonInRectItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 120, 90))
        self.setBrush(QBrush(QColor("#f1c40f")))
        self.item_type = "triangle"
        self.color = self.brush().color()

    def _polygon(self) -> QPolygonF:
        r = self.rect()
        return QPolygonF(
            [
                QPointF(r.left(), r.bottom()),
                QPointF(r.right(), r.bottom()),
                QPointF(r.center().x(), r.top()),
            ]
        )


class DiamondItem(_PolygonInRectItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 120, 90))
        self.setBrush(QBrush(QColor("#e74c3c")))
        self.item_type = "diamond"
        self.color = self.brush().color()

    def _polygon(self) -> QPolygonF:
        r = self.rect()
        cx = r.center().x()
        cy = r.center().y()
        return QPolygonF(
            [
                QPointF(cx, r.top()),
                QPointF(r.right(), cy),
                QPointF(cx, r.bottom()),
                QPointF(r.left(), cy),
            ]
        )


class HexagonItem(_PolygonInRectItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 140, 80))
        self.setBrush(QBrush(QColor("#2980b9")))
        self.item_type = "hexagon"
        self.color = self.brush().color()

    def _polygon(self) -> QPolygonF:
        r = self.rect()
        x0, x1 = r.left(), r.right()
        y0, y1 = r.top(), r.bottom()
        dx = (x1 - x0) * 0.25
        return QPolygonF(
            [
                QPointF(x0 + dx, y0),
                QPointF(x1 - dx, y0),
                QPointF(x1, (y0 + y1) / 2.0),
                QPointF(x1 - dx, y1),
                QPointF(x0 + dx, y1),
                QPointF(x0, (y0 + y1) / 2.0),
            ]
        )


class StarItem(_PolygonInRectItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 120, 120))
        self.setBrush(QBrush(QColor("#d35400")))
        self.item_type = "star"
        self.color = self.brush().color()

    def _polygon(self) -> QPolygonF:
        r = self.rect()
        cx = r.center().x()
        cy = r.center().y()
        outer = min(r.width(), r.height()) * 0.5
        inner = outer * 0.45

        points: list[QPointF] = []
        # 5-point star (10 vertices alternating outer/inner)
        import math

        for i in range(10):
            ang = -math.pi / 2.0 + i * (math.pi / 5.0)
            rad = outer if i % 2 == 0 else inner
            points.append(QPointF(cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
        return QPolygonF(points)
