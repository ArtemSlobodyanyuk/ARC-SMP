import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QLabel,
    QPushButton,
    QToolBar
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor, QAction


class CubeItem(QGraphicsRectItem):
    def __init__(self, size=100):
        super().__init__(QRectF(0, 0, size, size))

        self.setBrush(QBrush(QColor("#4CAF50")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable, True)

        self.name = "cube"
        self.note = ""

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            dialog = PropertyDialog(self)
            dialog.exec()
        super().mousePressEvent(event)


class PropertyDialog(QDialog):
    def __init__(self, cube):
        super().__init__()

        self.cube = cube
        self.setWindowTitle("Object properties")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Назва"))
        self.name_input = QLineEdit(cube.name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Нотатка"))
        self.note_input = QTextEdit(cube.note)
        layout.addWidget(self.note_input)

        save_button = QPushButton("Зберегти")
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save(self):
        self.cube.name = self.name_input.text()
        self.cube.note = self.note_input.toPlainText()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARCnGMS prototype")
        self.setGeometry(200, 200, 900, 600)

        # Сцена
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Верхня панель
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        add_action = QAction("Додати об'єкт", self)
        add_action.triggered.connect(self.add_cube)

        toolbar.addAction(add_action)

        # Стартовий куб
        self.add_cube()

    def add_cube(self):
        cube = CubeItem()
        cube.setPos(200, 200)
        self.scene.addItem(cube)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())