from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt

class Canvas(QGraphicsView):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(self.RenderHint.Antialiasing)

        # Відмалювати існуючі entity
        self.draw_entities()

        self.selected_item = None
        self.offset_x = 0
        self.offset_y = 0

    def draw_entities(self):
        self.scene.clear()
        for entity in self.core.scene.entities:
            rect = QGraphicsRectItem(0, 0, 32, 32)
            rect.setPos(entity.x, entity.y)
            rect.setBrush(Qt.GlobalColor.green)
            rect.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(rect)

    def mouseMoveEvent(self, event):
        if self.selected_item:
            pos = self.mapToScene(event.position().toPoint())
            x, y = self.core.placement.snap(pos.x() - self.offset_x, pos.y() - self.offset_y)
            self.selected_item.setPos(x, y)

    def mousePressEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        if item:
            self.selected_item = item
            self.offset_x = event.position().x() - item.pos().x()
            self.offset_y = event.position().y() - item.pos().y()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.selected_item = None
        super().mouseReleaseEvent(event)