import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.gui.MainWindow import MainWindow
from resources import resources_qrc  # noqa: F401
from src.session.SessionData import SessionData

myappid = "com.deeprook.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("DeepRook")
    app.setWindowIcon(QIcon(":/app_logo.ico"))
    app.setStyle("Fusion")

    session_data = SessionData()

    window = MainWindow(app=app, session_data=session_data)
    window.show()
    sys.exit(app.exec())
