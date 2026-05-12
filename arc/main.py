import sys
from PyQt6.QtWidgets import QApplication
from arc.ui.main_window import MainWindow
from arc.ui.start_menu import StartMenuWindow

def _ensure_app() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def run_editor(load_path: str | None = None) -> int:
    app = _ensure_app()

    window = MainWindow()
    if load_path:
        window.load_scene_from_file(load_path)
    window.show()

    return app.exec()

def run_menu() -> int:
    app = _ensure_app()

    window = StartMenuWindow()
    window.show()

    return app.exec()

def main() -> None:
    raise SystemExit(run_menu())

if __name__ == "__main__":
    main()
