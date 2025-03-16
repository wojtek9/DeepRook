from PySide6.QtWidgets import QFrame, QSizePolicy


def get_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    separator.setFrameShadow(QFrame.Shadow.Plain)
    separator.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    separator.setStyleSheet("border-left: 0.3px solid;  background: transparent; color: #303030;")
    return separator


def toggle_layout_widgets_enabled(layout, enabled: bool = None):
    if layout is not None:
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                if enabled is not None:
                    widget.setEnabled(enabled)
                else:
                    widget.setEnabled(not widget.isEnabled())


def toggle_layout_widgets_visible(layout, visible: bool = None):
    if layout is not None:
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                if visible is not None:
                    widget.setVisible(visible)
                else:
                    widget.setVisible(not widget.isVisible())
