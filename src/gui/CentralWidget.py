from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from src.gui.controlsview.ControlsView import ControlsView
from src.gui.logview.LogView import LogView
from src.gui.rookception.RookceptionView import RookceptionView
from src.gui.userscreen.UserScreen import UserScreenView
from src.utils import uiutils


class CentralWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.views_layout = QHBoxLayout()
        self.views_layout.setContentsMargins(0, 0, 0, 0)
        self.views_layout.setSpacing(0)

        # Controls View
        self.controls_view = ControlsView()
        #self.controls_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.controls_view.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # User Screen View
        self.user_screen_view = UserScreenView()
        #self.user_screen_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.user_screen_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Right Layout (Rookception & Log)
        right_layout = QVBoxLayout()
        self.rookception_view = RookceptionView()
        #self.rookception_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        self.log_view = LogView()
        #self.log_view.setStyleSheet("border: 1px solid gray; padding: 5px;")
        right_layout.addWidget(self.rookception_view)
        right_layout.addWidget(self.log_view)

        right_container = QWidget()
        right_container.setLayout(right_layout)
        #right_container.setStyleSheet("border: 1px solid gray; padding: 5px;")
        right_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.views_layout.addWidget(self.controls_view)
        self.views_layout.addWidget(uiutils.get_separator())
        self.views_layout.addWidget(self.user_screen_view, stretch=2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.views_layout.addWidget(uiutils.get_separator())
        self.views_layout.addWidget(right_container, stretch=1)

        self.main_layout.addLayout(self.views_layout)
