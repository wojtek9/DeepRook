import os

import cv2
import numpy as np
import mss
from PySide6.QtCore import QTimer, QObject, Signal

from src.logger.AppLogger import AppLogger
from src.utils import utils


class ScreenCapture(QObject):
    frameCaptured = Signal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sct = mss.mss()  # Screen capture instance
        self._monitor = 1
        self._fps = 30
        self._timer = QTimer(self)
        self._timer.setInterval(self._fps)
        self._timer.timeout.connect(self._capture_screen)

    def set_monitor(self, index: int):
        self._monitor = index
        AppLogger.debug(f"Monitor changed: {index}")

    def get_monitor(self) -> int:
        return self._monitor

    def set_fps(self, fps):
        self._fps = fps
        update_ms = self._fps_to_ms(fps)
        self._timer.setInterval(update_ms)
        AppLogger.debug(f"Set update rate to: {update_ms} ms")

    def start_recording(self):
        self._timer.start()
        AppLogger.debug("Started screen capture")

    def stop_recording(self):
        self._timer.stop()
        AppLogger.debug("Stopped screen capture")

    def capture_static_image(self, x, y, w, h):
        img_path = os.path.normpath(os.path.join(utils.get_temp_dir(), "DRSSimg.png"))
        monitor = {"top": y, "left": x, "width": w, "height": h}

        screenshot = self._sct.grab(monitor)  # Capture the selected region
        img = np.array(screenshot)  # Convert to NumPy array
        # img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        cv2.imwrite(img_path, img)  # Save image to file
        print(f"Saved chessboard image: {img_path}")
        return img_path

    def _capture_screen(self):
        # Capture the screen and emit the frame as a NumPy array
        monitor = self._sct.monitors[self._monitor]
        screen = self._sct.grab(monitor)

        # Convert to NumPy array & RGB format
        img = np.array(screen)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        self.frameCaptured.emit(img)

    @staticmethod
    def get_monitor_list():
        # Detect available monitors and return a list of monitor names
        with mss.mss() as sct:
            return [f"Monitor {i}" for i in range(1, len(sct.monitors))]

    @staticmethod
    def _fps_to_ms(fps):
        return int(1000 / fps)
