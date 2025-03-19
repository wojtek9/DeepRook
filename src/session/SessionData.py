from dataclasses import asdict

from PySide6.QtCore import QObject, Signal
from typing import Optional, Tuple

from src.core.dataclasses.BotParams import BotParams
from src.core.enums.Hotkeys import Hotkey


class SessionData(QObject):
    selectedRegionChanged = Signal(tuple)
    gameStateChanged = Signal(str)
    botEnabledChanged = Signal(bool)
    botParamsChanged = Signal(dict)
    engineChanged = Signal(str)
    engineRatingChanged = Signal(int)
    humanLikeMovementsChanged = Signal(bool)
    tempChessboardImageChanged = Signal(str)
    playAsWhiteChanged = Signal(bool)
    autoDetectionChanged = Signal(bool)
    autoMoveChanged = Signal(bool)
    nextMoveChanged = Signal(str)
    hotkeysUdapted = Signal()

    def __init__(self):
        super().__init__()
        self.bot_params: BotParams = BotParams()
        self.hotkeys: dict[Hotkey, str] = {}
        self._selected_region: Optional[Tuple[int, int, int, int]] = None
        self._play_as_white: bool = True
        self._game_state: str = "Not Started"
        self._bot_enabled: bool = False
        self._selected_engine: str = "Stockfish"
        self._engine_rating: int = 1200
        self._temp_chessboard_image: Optional[str] = None
        self._model_path: str = ""
        self.__next_move: str = ""

    def emit_hotkeys_updated(self):
        self.hotkeysUdapted.emit()

    @property
    def play_as_white(self):
        return self._play_as_white

    @play_as_white.setter
    def play_as_white(self, value: bool):
        if self._play_as_white != value:
            self._play_as_white = value
            self.playAsWhiteChanged.emit(value)

    @property
    def selected_region(self):
        return self._selected_region

    @selected_region.setter
    def selected_region(self, value: Tuple[int, int, int, int]):
        if self._selected_region != value:
            self._selected_region = value
            self.selectedRegionChanged.emit(value)

    @property
    def next_move(self):
        return self.__next_move

    @next_move.setter
    def next_move(self, value: str):
        if self.__next_move != value:
            self.__next_move = value
        self.nextMoveChanged.emit(value)

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value: str):
        if self._game_state != value:
            self._game_state = value
            self.gameStateChanged.emit(value)

    @property
    def bot_enabled(self):
        return self._bot_enabled

    @bot_enabled.setter
    def bot_enabled(self, value: bool):
        if self._bot_enabled != value:
            self._bot_enabled = value
            self.botEnabledChanged.emit(value)

    @property
    def selected_engine(self):
        return self._selected_engine

    @selected_engine.setter
    def selected_engine(self, value: str):
        if self._selected_engine != value:
            self._selected_engine = value
            self.engineChanged.emit(value)

    @property
    def engine_rating(self):
        return self._engine_rating

    @engine_rating.setter
    def engine_rating(self, value: int):
        if self._engine_rating != value:
            self._engine_rating = value
            self.engineRatingChanged.emit(value)

    @property
    def auto_detection(self):
        return self.bot_params.auto_detection

    @auto_detection.setter
    def auto_detection(self, value: bool):
        if self.bot_params.auto_detection != value:
            self.bot_params.auto_detection = value
            self.autoDetectionChanged.emit(value)

    @property
    def auto_move(self):
        return self.bot_params.auto_move

    @auto_move.setter
    def auto_move(self, value: bool):
        if self.bot_params.auto_move != value:
            self.bot_params.auto_move = value
            self.autoMoveChanged.emit(value)

    @property
    def human_like_movements(self):
        return self.bot_params.human_mouse_movements

    @human_like_movements.setter
    def human_like_movements(self, value: bool):
        if self.bot_params.human_mouse_movements != value:
            self.bot_params.human_mouse_movements = value
            self.humanLikeMovementsChanged.emit(value)

    @property
    def temp_chessboard_image(self):
        return self._temp_chessboard_image

    @temp_chessboard_image.setter
    def temp_chessboard_image(self, value: Optional[str]):
        if self._temp_chessboard_image != value:
            self._temp_chessboard_image = value
            self.tempChessboardImageChanged.emit(value)

    @property
    def model_path(self):
        return self._model_path

    @model_path.setter
    def model_path(self, value: str):
        if self._model_path != value:
            self._model_path = value
