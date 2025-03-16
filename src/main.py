import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.gui.MainWindow import MainWindow
from resources import resources_qrc  # noqa: F401

myappid = "com.deeprook.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("DeepRook")
    app.setWindowIcon(QIcon(":/app_logo.ico"))
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
