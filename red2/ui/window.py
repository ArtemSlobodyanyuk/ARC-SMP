from PyQt6.QtWidgets import QMainWindow, QApplication
from red2.ui.canvas import Canvas
import sys

class Window(QMainWindow):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setWindowTitle("бета map editor")
        self.setGeometry(100, 100, 800, 600)

        # Канвас
        self.canvas = Canvas(core)
        self.setCentralWidget(self.canvas)

        self.show()

if __name__ == "__main__":
    from red2.core.core import Core
    core = Core()
    app = QApplication(sys.argv)
    win = Window(core)
    sys.exit(app.exec())