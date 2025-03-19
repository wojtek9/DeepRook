import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src import PrepareApp
from src.gui.MainWindow import MainWindow
from resources import resources_qrc  # noqa: F401

# Remove?:
myappid = "com.deeprook.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("DeepRook")
    app.setWindowIcon(QIcon(":/icn/app_logo.ico"))

    session, config_manager = PrepareApp.prepare_app()

    window = MainWindow(app=app, session_data=session, config_manager=config_manager)
    window.show()
    sys.exit(app.exec())
