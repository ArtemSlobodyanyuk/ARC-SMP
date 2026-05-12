from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton,
    QColorDialog,
)
from PyQt6.QtGui import QColor


class PropertyDialog(QDialog):

    saved = pyqtSignal(object)

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

        layout.addWidget(QLabel("Width"))
        self.width_input = QLineEdit(str(obj.rect().width()))
        layout.addWidget(self.width_input)

        layout.addWidget(QLabel("Height"))
        self.height_input = QLineEdit(str(obj.rect().height()))
        layout.addWidget(self.height_input)

        layout.addWidget(QLabel("Color (hex)"))
        color_row = QHBoxLayout()
        self.color_input = QLineEdit(getattr(obj, "color", QColor("#3498db")).name(QColor.NameFormat.HexRgb))
        pick_button = QPushButton("Pick…")
        pick_button.clicked.connect(self.pick_color)
        color_row.addWidget(self.color_input)
        color_row.addWidget(pick_button)
        layout.addLayout(color_row)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        layout.addWidget(save_button)
        layout.addWidget(delete_button)
        self.setLayout(layout)

    def pick_color(self):
        initial = QColor(self.color_input.text())
        if not initial.isValid():
            initial = QColor("#3498db")
        chosen = QColorDialog.getColor(initial, self, "Pick color")
        if chosen.isValid():
            self.color_input.setText(chosen.name(QColor.NameFormat.HexRgb))

    def save(self):
        self.obj.name = self.name_input.text()
        self.obj.note = self.note_input.toPlainText()

        try:
            w = float(self.width_input.text())
            h = float(self.height_input.text())
            self.obj.resize(w, h)
        except:
            pass

        color = self.color_input.text().strip()
        if color:
            try:
                self.obj.color = color
            except Exception:
                pass

        self.saved.emit(self.obj)

    def delete(self):
        if self.obj:
            scene = self.obj.scene()
            if scene:
                scene.removeItem(self.obj)

            # повне очищення
            del self.obj
            self.obj = None

        self.accept()
