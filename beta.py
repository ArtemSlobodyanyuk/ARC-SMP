import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QLabel,
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor


class CubeItem(QGraphicsRectItem):
    def __init__(self, size=100):
        super().__init__(QRectF(0, 0, size, size))
        self.setBrush(QBrush(QColor("#FFFFFF")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.name = "cube"
        self.note = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARCnGMS Prototype")
        self.setGeometry(200, 200, 900, 600)

        # Центральний віджет
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        # Сцена
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view, 3)

        # Куб
        self.cube = CubeItem()
        self.cube.setPos(200, 200)
        self.scene.addItem(self.cube)

        # Панель властивостей
        panel = QVBoxLayout()

        panel.addWidget(QLabel("Назва:"))
        self.name_input = QLineEdit(self.cube.name)
        panel.addWidget(self.name_input)

        panel.addWidget(QLabel("Нотатка:"))
        self.note_input = QTextEdit(self.cube.note)
        panel.addWidget(self.note_input)

        layout.addLayout(panel, 1)

        # Сигнали
        self.name_input.textChanged.connect(self.update_name)
        self.note_input.textChanged.connect(self.update_note)

    def update_name(self, text):
        self.cube.name = text

    def update_note(self):
        self.cube.note = self.note_input.toPlainText()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())