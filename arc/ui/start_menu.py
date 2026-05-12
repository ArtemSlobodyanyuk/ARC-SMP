from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from arc.ui.main_window import MainWindow
from arc.ui.mods_window import ModsWindow


class StartMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARC platform")
        self.resize(720, 420)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        title = QLabel("ARC Platform")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        subtitle = QLabel("Оберіть модуль для запуску.")
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(10)

        open_editor = QPushButton("Редактор полотна")
        open_editor.clicked.connect(self._open_editor)

        open_scene = QPushButton("Відкрити сцену…")
        open_scene.clicked.connect(self._open_scene)

        mods_btn = QPushButton("Моди…")
        mods_btn.clicked.connect(self._open_mods)

        exit_btn = QPushButton("Вихід")
        exit_btn.clicked.connect(self.close)

        buttons_row.addWidget(open_editor)
        buttons_row.addWidget(open_scene)
        buttons_row.addWidget(mods_btn)
        buttons_row.addStretch(1)
        buttons_row.addWidget(exit_btn)

        layout.addLayout(buttons_row)

        hint = QLabel(
            "Підказка: це стартове меню — далі тут можна додати модулі "
            "(керування проєктами, бібліотеку обʼєктів, плагіни, налаштування)."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("margin-top: 8px;")
        layout.addWidget(hint)

        self.setCentralWidget(root)

        self._editor_window: MainWindow | None = None

    def _open_editor(self) -> None:
        self._show_editor(None)

    def _open_scene(self) -> None:
        saves_dir = Path(__file__).resolve().parents[2] / "saves"
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load scene",
            str(saves_dir),
            "JSON (*.json)",
        )
        if not filename:
            return
        self._show_editor(filename)

    def _show_editor(self, load_path: str | None) -> None:
        self._editor_window = MainWindow()
        if load_path:
            self._editor_window.load_scene_from_file(load_path)
        self._editor_window.show()
        self.hide()

        # If user closes editor, show menu again.
        def _on_editor_closed() -> None:
            self._editor_window = None
            self.show()

        self._editor_window.destroyed.connect(_on_editor_closed)  # type: ignore[arg-type]

    def _open_mods(self) -> None:
        dlg = ModsWindow(self)
        dlg.exec()
