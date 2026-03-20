import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QToolBar,
    QMenu,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QToolButton
)
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import QRectF


# ---------- Property Window ----------

class PropertyDialog(QDialog):

    def __init__(self, obj):
        super().__init__()

        self.obj = obj
        self.setWindowTitle("Object properties")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Name"))
        self.name_input = QLineEdit(obj.name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Note"))
        self.note_input = QTextEdit(obj.note)
        layout.addWidget(self.note_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)
        self.setLayout(layout)

    def save(self):
        self.obj.name = self.name_input.text()
        self.obj.note = self.note_input.toPlainText()
        self.close()


# ---------- Base Object ----------

class BaseItem:

    def init_object(self):
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        self.name = "object"
        self.note = ""

    def mouseDoubleClickEvent(self, event):
        dialog = PropertyDialog(self)
        dialog.exec()


# ---------- Shapes ----------

class CircleItem(QGraphicsEllipseItem, BaseItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 80, 80))
        self.setBrush(QBrush(QColor("#3498db")))
        self.init_object()


class SquareItem(QGraphicsRectItem, BaseItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 80, 80))
        self.setBrush(QBrush(QColor("#2ecc71")))
        self.init_object()


class RectangleItem(QGraphicsRectItem, BaseItem):

    def __init__(self):
        super().__init__(QRectF(0, 0, 120, 70))
        self.setBrush(QBrush(QColor("#e67e22")))
        self.init_object()


# ---------- Main Window ----------

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARC prototype")
        self.resize(900, 600)

        # Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Dropdown button
        add_button = QToolButton()
        add_button.setText("Add items")
        add_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        # Menu
        menu = QMenu()

        menu.addAction("Circle", self.add_circle)
        menu.addAction("Square", self.add_square)
        menu.addAction("Rectangle", self.add_rectangle)

        add_button.setMenu(menu)

        toolbar.addWidget(add_button)

    def add_circle(self):
        obj = CircleItem()
        obj.setPos(200, 200)
        self.scene.addItem(obj)

    def add_square(self):
        obj = SquareItem()
        obj.setPos(200, 200)
        self.scene.addItem(obj)

    def add_rectangle(self):
        obj = RectangleItem()
        obj.setPos(200, 200)
        self.scene.addItem(obj)


# ---------- Run ----------

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()