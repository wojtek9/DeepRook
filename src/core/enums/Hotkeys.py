from enum import IntEnum, auto


class Hotkey(IntEnum):
    GET_NEXT_MOVE = auto()
    MAKE_NEXT_MOVE = auto()
    INCREASE_DEPTH = auto()
    DECREASE_DEPTH = auto()
