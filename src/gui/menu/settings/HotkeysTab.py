from enum import IntEnum

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolButton,
    QApplication,
)
from PySide6.QtGui import QKeyEvent, QKeySequence, QIcon, QMouseEvent
from PySide6.QtCore import Qt, Signal

from src.core.enums.Hotkeys import Hotkey


class HotkeyRowAction(IntEnum):
    ACCEPT = 1
    BLOCK = 2
    CLEAR = 3


class HotkeyRowData:
    def __init__(self, description: str):
        self.description = description
        self.hotkey_bind = ""
        self.line_edit: HotkeyLineEdit | None = None
        self.accept_btn: QToolButton | None = None
        self.block_btn: QToolButton | None = None
        self.clear_btn: QToolButton | None = None


class HotkeyLineEdit(QLineEdit):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.pressed_keys = []

        # make an accept btn to then clear self.pressed_keys and register the shortcut
        # and remove btn to clear the hotkey

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit()
        super().mousePressEvent(event)

    def clear_field(self):
        self.pressed_keys.clear()
        self.clear()

    def keyPressEvent(self, event: QKeyEvent):
        event.accept()  # Stop QLineEdit from processing key events like CTRL+A

        readable_key = self.get_readable_key(event.key())
        if readable_key not in self.pressed_keys:
            self.pressed_keys.append(readable_key)
            hotkey_str = " + ".join(self.pressed_keys)
            self.setText(hotkey_str)

    @staticmethod
    def get_readable_key(key):
        # Convert event.key() to human-readable key name
        key_map = {
            Qt.Key.Key_Control: "CTRL",
            Qt.Key.Key_Shift: "SHIFT",
            Qt.Key.Key_Alt: "ALT",
            Qt.Key.Key_Meta: "META",  # Windows key / Command key on macOS
        }

        if key in key_map:
            return key_map[key]

        readable_key = QKeySequence(key).toString()

        return readable_key if readable_key else str(key)

    def keyReleaseEvent(self, event: QKeyEvent):
        event.accept()


class HotkeysTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.grid_layout = QGridLayout()
        self.registered_hotkeys: dict[Hotkey, str] = {}

        self.hotkey_rows: dict[Hotkey, HotkeyRowData] = {
            Hotkey.GET_NEXT_MOVE: HotkeyRowData("Get Next Move From Engine"),
            Hotkey.MAKE_NEXT_MOVE: HotkeyRowData("Make Next Move With Bot"),
            Hotkey.INCREASE_DEPTH: HotkeyRowData("Increase Engine Depth"),
            Hotkey.DECREASE_DEPTH: HotkeyRowData("Decrease Engine Depth"),
        }

        # Create fields for each hotkey
        for row, (hotkey, row_data) in enumerate(self.hotkey_rows.items()):
            label = QLabel(row_data.description)

            line_edit = HotkeyLineEdit(self)

            accept_btn = QToolButton()
            accept_btn.setEnabled(False)
            accept_btn.setIcon(QIcon(":/icn/checkmark_icon"))
            accept_btn.clicked.connect(
                lambda _, hk=hotkey, act=HotkeyRowAction.ACCEPT: self._handle_hotkey_row(hk, act)
            )
            line_edit.textChanged.connect(
                lambda text, btn=accept_btn: btn.setEnabled(bool(text.strip() and text.strip() != row_data.hotkey_bind))
            )
            line_edit.clicked.connect(lambda rd=row_data: self._line_edit_clicked(row_data))

            block_btn = QToolButton()
            block_btn.setIcon(QIcon(":/icn/block_icon"))
            block_btn.clicked.connect(lambda _, hk=hotkey, act=HotkeyRowAction.BLOCK: self._handle_hotkey_row(hk, act))

            clear_btn = QToolButton()
            clear_btn.setIcon(QIcon(":/icn/delete_icon"))
            clear_btn.clicked.connect(lambda _, hk=hotkey, act=HotkeyRowAction.CLEAR: self._handle_hotkey_row(hk, act))
            # line_edit.setPlaceholderText("Click to set hotkey")
            # line_edit.installEventFilter(self)  # Enable event filtering

            row_data.line_edit = line_edit
            row_data.accept_btn = accept_btn
            row_data.block_btn = block_btn
            row_data.clear_btn = clear_btn

            self.grid_layout.addWidget(label, row, 0)
            self.grid_layout.addWidget(line_edit, row, 1)
            self.grid_layout.addWidget(accept_btn, row, 2)
            self.grid_layout.addWidget(block_btn, row, 3)
            self.grid_layout.addWidget(clear_btn, row, 4)

        main_layout.addLayout(self.grid_layout)

    def set_config(self):
        pass
        # REMEMBER TO USE BLOCKSIGNALS WHEN SETTING CONFIG SO ACCEPT BTN DOESNT GET ENABLED
        # line_edit.blockSignals(True)
        # line_edit.setText(saved_hotkey)  # Set text without firing textChanged
        # line_edit.blockSignals(False)

    def clear_unset_hotkey_fields(self):
        for hotkey, row_data in self.hotkey_rows.items():
            if not row_data.hotkey_bind.strip():
                row_data.line_edit.clear_field()

    def get_hotkey_bind_from_enum(self, action: Hotkey):
        return self.registered_hotkeys.get(action, None)

    def _line_edit_clicked(self, clicked_row_data: HotkeyRowData):
        for row in self.hotkey_rows.values():
            if row.hotkey_bind.strip():
                row.line_edit.setText(row.hotkey_bind.strip())
        if clicked_row_data.hotkey_bind.strip():
            clicked_row_data.line_edit.setText("")

    def _handle_hotkey_row(self, hotkey: Hotkey, action: HotkeyRowAction):
        line_edit = self.hotkey_rows[hotkey].line_edit
        if action == HotkeyRowAction.ACCEPT:
            self.hotkey_rows[hotkey].hotkey_bind = line_edit.text().strip()
            self.hotkey_rows[hotkey].accept_btn.setEnabled(False)
        elif action == HotkeyRowAction.BLOCK:
            pass
        elif action == HotkeyRowAction.CLEAR:
            self.hotkey_rows[hotkey].hotkey_bind = ""
            line_edit.clear_field()
        self.clear_focused_widgets()

    @staticmethod
    def clear_focused_widgets():
        try:
            focused_widget = QApplication.focusWidget()
            if focused_widget:
                focused_widget.clearFocus()
        except Exception:
            pass

    def mousePressEvent(self, event):
        try:
            self.clear_unset_hotkey_fields()
            self.clear_focused_widgets()
        except Exception:
            pass
        finally:
            super().mousePressEvent(event)

    # def eventFilter(self, obj, event):
    #     """Intercept clicks on QLineEdit to start key capture."""
    #     if event.type() == QEvent.Type.MouseButtonPress and obj in self.hotkey_fields.values():
    #         self.capture_hotkey(obj)
    #         return True
    #
    #     return super().eventFilter(obj, event)

    # def capture_hotkey(self, line_edit):
    #     """Start listening for key presses when the field is clicked."""
    #     self.active_hotkey_field = line_edit
    #     self.pressed_keys.clear()
    #     line_edit.grabKeyboard()  # Capture keyboard input
    #
    # @staticmethod
    # def get_readable_key(key):
    #     # Convert event.key() to human-readable key name
    #     key_map = {
    #         Qt.Key.Key_Control: "CTRL",
    #         Qt.Key.Key_Shift: "SHIFT",
    #         Qt.Key.Key_Alt: "ALT",
    #         Qt.Key.Key_Meta: "META",  # Windows key / Command key on macOS
    #     }
    #
    #     if key in key_map:
    #         return key_map[key]
    #
    #     readable_key = QKeySequence(key).toString()
    #
    #     return readable_key if readable_key else str(key)
    #
    # def keyPressEvent(self, event: QKeyEvent):
    #     """Capture the pressed keys and store them in order."""
    #     if not self.active_hotkey_field:
    #         return
    #
    #     key = event.key()
    #     modifiers = event.modifiers()
    #
    #     self.active_hotkey_field.setText(self.get_readable_key(key))
    #
    #     # Track modifiers in the order they are pressed
    #     if modifiers & Qt.KeyboardModifier.ControlModifier and "CTRL" not in self.pressed_keys:
    #         self.pressed_keys.append("CTRL")
    #     if modifiers & Qt.KeyboardModifier.AltModifier and "ALT" not in self.pressed_keys:
    #         self.pressed_keys.append("ALT")
    #     if modifiers & Qt.KeyboardModifier.ShiftModifier and "SHIFT" not in self.pressed_keys:
    #         self.pressed_keys.append("SHIFT")
    #
    #     # Store normal key (ignoring standalone modifiers)
    #     key_name = event.text().upper()
    #     if key_name and key_name not in ["CTRL", "ALT", "SHIFT"] and key_name not in self.pressed_keys:
    #         self.pressed_keys.append(key_name)
    #     print(self.pressed_keys)
    #
    # def keyReleaseEvent(self, event: QKeyEvent):
    #     """Register hotkey only after all keys are released."""
    #     if not self.active_hotkey_field:
    #         return
    #
    #     # Convert pressed keys list to a formatted hotkey string
    #     hotkey_str = " + ".join(self.pressed_keys) if self.pressed_keys else "Invalid Key"
    #
    #     # Set the hotkey in the field
    #     self.active_hotkey_field.setText(hotkey_str)
    #     self.field_registered_hotkeys[self.active_hotkey_field] = hotkey_str
    #
    #     # Stop capturing keyboard input
    #     self.active_hotkey_field.releaseKeyboard()
    #     self.active_hotkey_field = None
    #     self.pressed_keys.clear()  # Clear for next capture
