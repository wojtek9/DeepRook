from dataclasses import dataclass
from src.core.enums.Hotkeys import Hotkey


@dataclass
class HotKeyBinds:
    Hotkey.GET_NEXT_MOVE = ""
    Hotkey.MAKE_NEXT_MOVE = ""
    Hotkey.INCREASE_DEPTH = ""
    Hotkey.DECREASE_DEPTH = ""
