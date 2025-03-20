from PySide6.QtCore import QObject

from src.bot import Mouse
from src.session.SessionData import SessionData


class ChessBot(QObject):
    def __init__(self, session_data: SessionData):
        super().__init__()
        self.session_data = session_data
        self.in_analysis = False
        self.move_delay_ms = session_data
        self.turn = "w" if session_data.play_as_white else "b"
        self.running = True

    def move_piece(self, move: str):
        Mouse.move_piece_hypersonic(move, self.session_data.selected_region)
