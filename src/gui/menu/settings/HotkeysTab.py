from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QApplication
from PySide6.QtGui import QKeyEvent, QPalette, QColor, QKeySequence
from PySide6.QtCore import Qt, QEvent


class HotkeysTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Grid layout for hotkey fields
        self.grid_layout = QGridLayout()
        self.hotkey_fields = {}
        self.field_registered_hotkeys = {}

        # Define hotkey actions
        self.hotkey_labels = [
            "Get Next Move From Engine",
            "Make Next Move With Bot",
            "Increase Engine Depth",
            "Decrease Engine Depth",
        ]

        # Create fields for each hotkey
        for row, label_text in enumerate(self.hotkey_labels):
            label = QLabel(label_text)
            line_edit = HotkeyLineEdit(self)
            # line_edit.setPlaceholderText("Click to set hotkey")
            line_edit.installEventFilter(self)  # Enable event filtering

            # Store reference to field
            self.hotkey_fields[label_text] = line_edit
            self.field_registered_hotkeys[line_edit] = ""

            # Add to grid layout
            self.grid_layout.addWidget(label, row, 0)
            self.grid_layout.addWidget(line_edit, row, 1)

        # Add grid layout to main layout
        main_layout.addLayout(self.grid_layout)

        # Track active field and pressed keys
        self.active_hotkey_field = None
        self.pressed_keys = []

    # def eventFilter(self, obj, event):
    #     """Intercept clicks on QLineEdit to start key capture."""
    #     if event.type() == QEvent.Type.MouseButtonPress and obj in self.hotkey_fields.values():
    #         self.capture_hotkey(obj)
    #         return True
    #
    #     return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        try:
            focused_widget = QApplication.focusWidget()
            if focused_widget:
                focused_widget.clearFocus()
        except Exception:
            pass
        finally:
            super().mousePressEvent(event)

    def set_hotkey_fields_text(self):
        for edit, text in self.field_registered_hotkeys.items():
            edit.setText(text)

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


class HotkeyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.pressed_keys = []

        # make an accept btn to then clear self.pressed_keys and register the shortcut
        # and remove btn to clear the hotkey

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
