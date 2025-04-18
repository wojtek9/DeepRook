from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            """
                QLineEdit:hover {
                    background-color: #31363b;
                }
            """
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()
