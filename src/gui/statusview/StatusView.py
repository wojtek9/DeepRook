from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.session.SessionData import SessionData


class StatusView(QWidget):
    def __init__(self, session_data: SessionData, parent=None):
        super().__init__()

        self._session_data = session_data

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(QLabel("STATUS"))