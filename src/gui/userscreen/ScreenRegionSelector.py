import cv2
import numpy as np
import mss
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QGuiApplication


class ScreenRegionSelector(QDialog):
    def __init__(self, monitor_index: int = 1):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        screens = QGuiApplication.screens()
        mss_monitors = mss.mss().monitors  # Get list of available monitors

        # Fix: Ensure index mapping between QScreen and mss
        self.qscreen_index = monitor_index - 1  # Convert mss index to QScreen index
        self.mss_monitor_index = monitor_index  # mss uses 1-based indexing

        if self.qscreen_index >= len(screens) or self.mss_monitor_index >= len(mss_monitors):
            print(f"Monitor {monitor_index} is out of range.")
            self.qscreen_index = 0  # Default to first screen
            self.mss_monitor_index = 1

        self.monitor_geometry = screens[self.qscreen_index].geometry()

        # Resize window to match selected monitor
        self.setGeometry(self.monitor_geometry)
        self.move(self.monitor_geometry.topLeft())

        # Capture screen
        self.screen = self.capture_screen()
        self.start_pos = None
        self.end_pos = None
        self.selection_rect = QRect()

    def capture_screen(self):
        # Capture the selected monitor using mss and convert to QPixmap
        with mss.mss() as sct:
            monitor = sct.monitors[self.mss_monitor_index]
            screen = sct.grab(monitor)

            img = np.array(screen)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

            height, width, _ = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

            return QPixmap.fromImage(q_img)

    def paintEvent(self, event):
        # Draw the screen overlay and selection rectangle
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.screen)

        # Dark transparent overlay ONLY on selected monitor
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))  # Semi-transparent black
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # Draw selection rectangle if user is selecting
        if not self.selection_rect.isNull():
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(255, 0, 0), 1))  # Red border
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event):
        # Start selection
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, QSize(0, 0))
            self.update()

    def mouseMoveEvent(self, event):
        # Update selection rectangle while dragging
        if self.start_pos:
            self.end_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, self.end_pos).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        # Save the selected region and close the selector
        if event.button() == Qt.MouseButton.LeftButton:
            x, y, w, h = (
                self.selection_rect.x(),
                self.selection_rect.y(),
                self.selection_rect.width(),
                self.selection_rect.height(),
            )
            self.selected_region = (x, y, w, h)
            self.accept()

    def get_selected_region(self):
        return getattr(self, "selected_region", None)
