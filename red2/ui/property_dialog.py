from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton
)


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

        layout.addWidget(QLabel("Width"))
        self.width_input = QLineEdit(str(obj.rect().width()))
        layout.addWidget(self.width_input)

        layout.addWidget(QLabel("Height"))
        self.height_input = QLineEdit(str(obj.rect().height()))
        layout.addWidget(self.height_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        layout.addWidget(save_button)
        self.setLayout(layout)

    def save(self):
        self.obj.name = self.name_input.text()
        self.obj.note = self.note_input.toPlainText()

        try:
            w = float(self.width_input.text())
            h = float(self.height_input.text())
            self.obj.resize(w, h)
        except:
            pass

        self.close()