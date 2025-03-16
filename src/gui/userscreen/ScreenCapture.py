import cv2
import numpy as np
import mss
from PySide6.QtCore import QTimer, QObject, Signal


class ScreenCapture(QObject):
    frameCaptured = Signal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sct = mss.mss()  # Screen capture instance
        self._fps = 30
        self._timer = QTimer(self)
        self._timer.setInterval(self._fps)
        self._timer.timeout.connect(self._capture_screen)

    def start_capturing(self):
        self._timer.start()

    def stop_capturing(self):
        self._timer.stop()

    def _capture_screen(self):
        """Capture the screen and emit the frame as a NumPy array."""
        monitor = self._sct.monitors[1]  # Capture primary monitor
        screen = self._sct.grab(monitor)

        # Convert to NumPy array & RGB format
        img = np.array(screen)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        self.frameCaptured.emit(img)
