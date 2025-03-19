from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from src.core.ConfigManager import ConfigManager
from src.gui.CentralWidget import CentralWidget
from src.gui.menu.MenuBar import MenuBar
from src.session.SessionData import SessionData


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, session_data: SessionData, config_manager: ConfigManager):
        super().__init__()

        self.app = app
        self.session_data = session_data
        self.config_manager = config_manager

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
        config = {
            "selected_region": self.session_data.selected_region,
            "play_as_white": self.session_data.play_as_white,
            "game_state": self.session_data.game_state,
            "bot_enabled": self.session_data.bot_enabled,
            "engine": self.session_data.selected_engine,
            "engine_rating": self.session_data.engine_rating,
            "human_like_movements": self.session_data.human_like_movements,
            "temp_chessboard_image": self.session_data.temp_chessboard_image,
            "model_path": self.session_data.model_path,
            "bot_params": {
                "start_delay": self.session_data.bot_params.start_delay,
                "human_mouse_movements": self.session_data.bot_params.human_mouse_movements,
                "random_move_delay": self.session_data.bot_params.random_move_delay,
                "min_move_delay": self.session_data.bot_params.min_move_delay,
                "max_move_delay": self.session_data.bot_params.max_move_delay,
                "auto_detection": self.session_data.bot_params.auto_detection,
                "auto_move": self.session_data.bot_params.auto_move,
            },
        }

        self.config_manager.set_config(config)
        event.accept()
