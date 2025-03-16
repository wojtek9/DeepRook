from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from src.gui.CentralWidget import CentralWidget
from src.gui.menu.MenuBar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self.app.setStyle("Fusion")

        self.setWindowTitle("DeepRook")
        self.setWindowIcon(QIcon(":/app_logo.ico"))
        self.setGeometry(560, 240, 800, 600)

        self.menu_bar = MenuBar(app=app, parent=self)
        self.setMenuBar(self.menu_bar)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
