import keyboard
from PySide6.QtCore import QObject, Signal
from src.session.SessionData import SessionData
from src.core.enums.Hotkeys import Hotkey


class HotkeyListener(QObject):
    hotkeyTriggered = Signal(Hotkey)

    def __init__(self, session_data: SessionData, parent=None):
        super().__init__(parent)
        self.session_data = session_data
        self.session_data.hotkeysUdapted.connect(self.update_hotkeys)
        self.active_hotkeys = {}
        self._register_hotkeys()

    def _register_hotkeys(self):
        self.clear_hotkeys()

        for hotkey_enum, keybind in self.session_data.hotkeys.items():
            if keybind:
                self._bind_hotkey(hotkey_enum, keybind)

    def _bind_hotkey(self, hotkey_enum: Hotkey, keybind: str):
        if keybind in self.active_hotkeys:
            keyboard.remove_hotkey(self.active_hotkeys[keybind])

        hotkey_id = keyboard.add_hotkey(keybind, lambda: self.hotkeyTriggered.emit(hotkey_enum))
        self.active_hotkeys[keybind] = hotkey_id

    def clear_hotkeys(self):
        for keybind in self.active_hotkeys.values():
            keyboard.remove_hotkey(keybind)
        self.active_hotkeys.clear()

    def update_hotkeys(self):
        self._register_hotkeys()
