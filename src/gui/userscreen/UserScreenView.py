import mss
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QSpinBox, QComboBox, QHBoxLayout, QCheckBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt

from src.gui.userscreen.ScreenCapture import ScreenCapture


class UserScreenView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Control Panel Layout
        self.controls_layout = QHBoxLayout()

        # Monitor Selection Dropdown
        self.monitor_selector = QComboBox()
        self.monitor_selector.addItems(self.get_monitor_list())
        self.monitor_selector.currentIndexChanged.connect(self.update_monitor)
        self.controls_layout.addWidget(self.monitor_selector)

        # FPS Selection
        self.fps_selector = QSpinBox()
        self.fps_selector.setRange(1, 60)
        self.fps_selector.setValue(30)  # Default 30 FPS
        self.fps_selector.valueChanged.connect(self.update_fps)
        self.controls_layout.addWidget(self.fps_selector)

        # Enable/Disable Screen Capture Checkbox
        self.capture_checkbox = QCheckBox("Enable Screen Capture")
        self.capture_checkbox.setChecked(False)
        self.capture_checkbox.toggled.connect(self.toggle_screen_capture)
        self.controls_layout.addWidget(self.capture_checkbox)

        self.layout.addLayout(self.controls_layout)

        # QLabel for displaying screen capture
        self.screen_label = QLabel(self)
        self.screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.screen_label)

        # Screen Capture instance
        self.screen_capture = ScreenCapture(self)
        self.screen_capture.frameCaptured.connect(self.update_screen)  # Listen for frames

    def update_screen(self, img):
        """Update QLabel with the new screen frame."""
        height, width, _ = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        # Scale and display in QLabel
        pixmap = QPixmap.fromImage(q_img)
        self.screen_label.setPixmap(
            pixmap.scaled(
                self.screen_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
        )

    def get_monitor_list(self):
        """Detect available monitors and return a list of monitor names."""
        with mss.mss() as sct:
            return [f"Monitor {i}" for i in range(1, len(sct.monitors))]

    def update_monitor(self, index):
        """Update the monitor used for screen capture."""
        self.screen_capture.monitor_index = index + 1

    def update_fps(self, value):
        """Update the FPS value for screen capture."""
        self.screen_capture._timer.setInterval(int(1000 / value))

    def toggle_screen_capture(self, enabled):
        """Enable or disable screen capturing."""
        if enabled:
            self.screen_capture.start_capturing()
        else:
            self.screen_capture.stop_capturing()
