from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from src.gui.CentralWidget import CentralWidget
from src.gui.menu.MenuBar import MenuBar
from src.session.SessionData import SessionData


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, session_data: SessionData):
        super().__init__()

        self.app = app
        self.session_data = session_data

        self.setWindowTitle("DeepRook")
        self.setWindowIcon(QIcon(":/icn/app_logo.ico"))
        self.setGeometry(560, 240, 800, 600)
        self.setMinimumSize(735, 480)

        self.menu_bar = MenuBar(app=app, parent=self)
        self.setMenuBar(self.menu_bar)

        self.central_widget = CentralWidget(parent=self, session_data=session_data)
        self.setCentralWidget(self.central_widget)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     print(self.size())

    def mousePressEvent(self, event):
        try:
            focused_widget = QApplication.focusWidget()
            if focused_widget:
                focused_widget.clearFocus()
        except Exception:
            pass
        finally:
            super().mousePressEvent(event)

    def closeEvent(self, event):
        pass