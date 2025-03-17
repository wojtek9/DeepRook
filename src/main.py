import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.gui.MainWindow import MainWindow
from resources import resources_qrc  # noqa: F401
from src.session.SessionData import SessionData
from src.utils import utils

# Remove?:
myappid = "com.deeprook.app"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def prepare_app(session):
    model_path = utils.get_model_path()
    session.model_path = model_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("DeepRook")
    app.setWindowIcon(QIcon(":/icn/app_logo.ico"))
    app.setStyle("Fusion")

    session_data = SessionData()
    prepare_app(session_data)

    window = MainWindow(app=app, session_data=session_data)
    window.show()
    sys.exit(app.exec())
