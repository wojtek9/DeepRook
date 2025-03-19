from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from src.core.HotkeyListener import HotkeyListener
from src.gui.controlsview.ControlsView import ControlsView
from src.gui.logview.LogView import LogView
from src.gui.rookception.RookceptionView import RookceptionView
from src.gui.statusview.StatusView import StatusView
from src.gui.userscreenview.UserScreenView import UserScreenView
from src.logger.AppLogger import AppLogger
from src.session.SessionData import SessionData
from src.utils import uiutils
import qdarktheme


class CentralWidget(QWidget):
    def __init__(self, parent, session_data: SessionData):
        super().__init__(parent)

        self.session_data = session_data
        qdarktheme.setup_theme("dark")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.views_layout = QHBoxLayout()
        self.views_layout.setContentsMargins(0, 0, 0, 0)
        self.views_layout.setSpacing(0)

        self.hotkeys_listener = HotkeyListener(session_data)

        # Controls View
        self.controls_view = ControlsView(session_data=session_data)
        # self.controls_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.controls_view.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # User Screen View
        # middle_container = QWidget()
        # middle_layout = QVBoxLayout()
        # self.status_view = StatusView(session_data=session_data)
        self.user_screen_view = UserScreenView(session_data=session_data, hotkey_listener=self.hotkeys_listener)
        self.user_screen_view.setMinimumSize(320, 240)
        # self.user_screen_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.user_screen_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # middle_layout.addWidget(self.status_view)
        # middle_layout.addWidget(self.user_screen_view)
        # middle_container.setLayout(middle_layout)

        # Right Layout (Rookception & Log)
        right_container = QWidget()
        right_layout = QVBoxLayout()
        self.rookception_view = RookceptionView()
        # self.rookception_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.log_view = LogView()
        # self.log_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        right_layout.addWidget(self.rookception_view)
        right_layout.addWidget(self.log_view)

        right_container.setLayout(right_layout)
        # right_container.setStyleSheet("border: 1px solid gray; padding: 5px;")
        right_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.views_layout.addWidget(self.controls_view)
        self.views_layout.addWidget(uiutils.get_separator())
        self.views_layout.addWidget(self.user_screen_view, stretch=2)
        self.views_layout.addWidget(uiutils.get_separator())
        self.views_layout.addWidget(right_container, stretch=1)

        self.main_layout.addLayout(self.views_layout)

        AppLogger.info("Application started.")
