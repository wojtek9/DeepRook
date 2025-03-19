from enum import IntEnum

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolButton,
    QApplication,
    QPushButton,
)
from PySide6.QtGui import QKeyEvent, QKeySequence, QIcon, QMouseEvent
from PySide6.QtCore import Qt, Signal, QTimer

from src.core.enums.Hotkeys import Hotkey
from src.session.SessionData import SessionData


class HotkeyRowAction(IntEnum):
    ACCEPT = 1
    BLOCK = 2
    CLEAR = 3


class HotkeyRowObject:
    def __init__(self, description: str, hotkey: Hotkey):
        self.description = description
        self.hotkey = hotkey
        self.hotkey_bind = ""

        self.line_edit = HotkeyLineEdit()
        self.accept_btn = self._create_button(":/icn/checkmark_icon", enabled=False)
        self.block_btn = self._create_button(":/icn/block_icon", enabled=False)
        self.clear_btn = self._create_button(":/icn/delete_icon", enabled=False)

        self.accept_btn.clicked.connect(self._on_accept_btn_clicked)
        self.block_btn.clicked.connect(self._on_block_btn_clicked)
        self.clear_btn.clicked.connect(self._on_clear_btn_clicked)

        self.line_edit.textChanged.connect(self._on_text_changed)
        self.line_edit.clicked.connect(self._on_line_edit_clicked)
        self.line_edit.focusOutEventTriggered.connect(self._on_line_edit_focus_out)

    @staticmethod
    def _create_button(icon_path: str, enabled=True) -> QToolButton:
        btn = QToolButton()
        btn.setIcon(QIcon(icon_path))
        btn.setEnabled(enabled)
        return btn

    def apply_line_edit_text_safe(self, text: str):
        self.line_edit.blockSignals(True)
        self.line_edit.setText(text)
        self.line_edit.blockSignals(False)

    def clear_focus(self):
        self.line_edit.clearFocus()
        self.accept_btn.clearFocus()
        self.block_btn.clearFocus()
        self.clear_btn.clearFocus()

    def _on_accept_btn_clicked(self):
        self.hotkey_bind = self.line_edit.text().strip()
        self.accept_btn.setEnabled(False)
        self.block_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.clear_focus()

    def _on_block_btn_clicked(self):
        pass

    def _on_clear_btn_clicked(self):
        self.hotkey_bind = ""
        self.line_edit.complete_clear()
        self.accept_btn.setEnabled(False)
        self.block_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.clear_focus()

    def _on_text_changed(self, text: str):
        if text.strip() and text.strip() != self.hotkey_bind.strip():
            self.accept_btn.setEnabled(True)
        if text.strip():
            self.clear_btn.setEnabled(True)

    def _on_line_edit_clicked(self):
        self.apply_line_edit_text_safe("")

    def _on_line_edit_focus_out(self):
        self.apply_line_edit_text_safe(self.hotkey_bind)
        self.accept_btn.setEnabled(False)
        if not self.hotkey_bind.strip():
            self.block_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)


class HotkeyLineEdit(QLineEdit):
    clicked = Signal()
    focusOutEventTriggered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.unsaved_hotkey_bind = ""
        self.pressed_keys = []

    def focusInEvent(self, event):
        self.blockSignals(True)
        self.setText("")
        self.blockSignals(False)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # Slight delay to avoid race condition when clicking accept btn
        QTimer.singleShot(100, self.focusOutEventTriggered.emit)
        super().focusOutEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit()
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        event.accept()

        readable_key = self.get_readable_key(event.key())
        if readable_key not in self.pressed_keys:
            self.pressed_keys.append(readable_key)
            self.setText(" + ".join(self.pressed_keys))

    def keyReleaseEvent(self, event: QKeyEvent):
        event.accept()
        self.unsaved_hotkey_bind = " + ".join(self.pressed_keys)
        self.pressed_keys.clear()

    def complete_clear(self):
        self.unsaved_hotkey_bind = ""
        self.clear_field()

    def clear_field(self):
        self.pressed_keys.clear()
        self.blockSignals(True)
        self.clear()
        self.blockSignals(False)

    @staticmethod
    def get_readable_key(key):
        key_map = {
            Qt.Key.Key_Control: "CTRL",
            Qt.Key.Key_Shift: "SHIFT",
            Qt.Key.Key_Alt: "ALT",
            Qt.Key.Key_Meta: "META",
        }

        return key_map.get(key, QKeySequence(key).toString() or str(key))


class HotkeysTab(QWidget):
    def __init__(self, session_data: SessionData, parent=None):
        super().__init__(parent)

        self.session_data = session_data

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.grid_layout = QGridLayout()
        self.registered_hotkeys: dict[Hotkey, str] = {}

        self.hotkey_row_objs: list[HotkeyRowObject] = [
            HotkeyRowObject(description="Get Next Move From Engine", hotkey=Hotkey.GET_NEXT_MOVE),
            HotkeyRowObject(description="Make Next Move With Bot", hotkey=Hotkey.MAKE_NEXT_MOVE),
            HotkeyRowObject(description="Increase Engine Depth", hotkey=Hotkey.INCREASE_DEPTH),
            HotkeyRowObject(description="Decrease Engine Depth", hotkey=Hotkey.DECREASE_DEPTH),
        ]

        self._setup_ui()
        main_layout.addLayout(self.grid_layout)

    def _setup_ui(self):
        for row, row_obj in enumerate(self.hotkey_row_objs):
            label = QLabel(row_obj.description)
            self.grid_layout.addWidget(label, row, 0)
            self.grid_layout.addWidget(row_obj.line_edit, row, 1)
            self.grid_layout.addWidget(row_obj.accept_btn, row, 2)
            self.grid_layout.addWidget(row_obj.block_btn, row, 3)
            self.grid_layout.addWidget(row_obj.clear_btn, row, 4)

    def save_hotkeys_to_session(self):
        pass

    @staticmethod
    def clear_focused_widgets():
        focused_widget = QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

    def mousePressEvent(self, event):
        self.clear_focused_widgets()
        super().mousePressEvent(event)

    def hideEvent(self, event):
        self.clear_focused_widgets()
        for row_obj in self.hotkey_row_objs:
            row_obj.clear_focus()
            row_obj.line_edit.setText(row_obj.hotkey_bind)
        self.save_hotkeys_to_session()
        super().hideEvent(event)

    def closeEvent(self, event):
        print("here")
        super().closeEvent(event)
