from enum import IntEnum, auto


class Hotkey(IntEnum):
    GET_NEXT_MOVE = auto()
    MAKE_NEXT_MOVE = auto()
    MAKE_BEST_MOVE = auto()
    MAKE_SECOND_BEST_MOVE = auto()
    MAKE_THIRD_BEST_MOVE = auto()
    MAKE_FOURTH_BEST_MOVE = auto()
    INCREASE_DEPTH = auto()
    DECREASE_DEPTH = auto()
