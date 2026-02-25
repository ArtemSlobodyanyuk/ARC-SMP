from PyQt6.QtWidgets import QApplication
from red2.core.core import Core
from red2.ui.window import Window
import sys

def main():
    core = Core(object_path="object", save_path="save")
    app = QApplication(sys.argv)
    window = Window(core)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()