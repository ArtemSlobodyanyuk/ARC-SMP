from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QToolBar,
    QMenu,
    QToolButton
)

from red2.core.factory import ObjectFactory


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARC prototype")
        self.resize(900, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.factory = ObjectFactory(self.scene)

        self.init_toolbar()

    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        add_button = QToolButton()
        add_button.setText("Add items")
        add_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        menu = QMenu()

        menu.addAction("Circle", lambda: self.factory.create("circle"))
        menu.addAction("Square", lambda: self.factory.create("square"))
        menu.addAction("Rectangle", lambda: self.factory.create("rectangle"))

        add_button.setMenu(menu)
        toolbar.addWidget(add_button)