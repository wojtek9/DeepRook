import os
import threading

import cv2
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QDialog,
    QGroupBox,
    QFormLayout,
)
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtCore import Qt, QRect

from src.CNNlayer.Rookception import Rookception
from src.bot.ChessBot import ChessBot
from src.gui.userscreenview.ScreenCapture import ScreenCapture
from src.gui.userscreenview.ScreenRegionSelector import ScreenRegionSelector
from src.logger.AppLogger import AppLogger
from src.session.SessionData import SessionData


class UserScreenView(QWidget):
    def __init__(self, session_data: SessionData, parent=None):
        super().__init__(parent)

        self.session_data = session_data
        self.session_data.selectedRegionChanged.connect(self.update_overlay)

        self._rookception: Rookception | None = None

        # Screen Capture instance
        self.screen_capture = ScreenCapture(self)
        self.screen_capture.frameCaptured.connect(self.update_live_screen)  # Listen for frames
        self.last_frame = None

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Screen Control Panel
        self.screen_control_panel = QGroupBox("Screen Capture Controls")
        self.screen_control_layout = QFormLayout(self.screen_control_panel)

        self.select_region_btn = QPushButton("Mark Chessboard Region")
        self.select_region_btn.clicked.connect(self._select_chessboard_region)
        self.screen_control_layout.addRow("Select Region:", self.select_region_btn)

        self.monitor_selector = QComboBox()
        self.monitor_selector.addItems(self.screen_capture.get_monitor_list())
        self.monitor_selector.currentIndexChanged.connect(self.update_monitor)
        self.screen_control_layout.addRow("Monitor:", self.monitor_selector)

        self.fps_selector = QSpinBox()
        self.fps_selector.setRange(1, 60)
        self.fps_selector.setValue(10)
        self.fps_selector.valueChanged.connect(self.update_fps)
        self.screen_control_layout.addRow("FPS:", self.fps_selector)

        self.capture_checkbox = QCheckBox("Enable Screen Capture")
        self.capture_checkbox.setChecked(False)
        self.capture_checkbox.toggled.connect(self.toggle_screen_capture)
        self.screen_control_layout.addRow("Live Capture:", self.capture_checkbox)

        # Engine Control Panel
        self.engine_control_panel = QGroupBox("Engine Controls")
        self.engine_control_layout = QVBoxLayout(self.engine_control_panel)
        self.get_best_move_btn = QPushButton("Get Best Move")
        self.get_best_move_btn.clicked.connect(self._on_get_next_move_clicked)
        self.engine_control_layout.addWidget(self.get_best_move_btn)

        self.main_layout.addWidget(self.screen_control_panel)
        self.main_layout.addWidget(self.engine_control_panel)

        # Label for displaying screen capture
        self.live_screen_label = QLabel(self)
        self.live_screen_label.setVisible(False)
        self.live_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.live_screen_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.live_screen_label)

        # Label for displaying captured region if screen capture is turned off
        self.static_screen_label = QLabel(self)
        self.static_screen_label.setVisible(True)
        self.static_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.static_screen_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.static_screen_label)

        self._initialize_rookception(session_data)


    def _load_rookception(self, model_path):
        self._rookception = Rookception(model_path)
        AppLogger.debug("CNN loaded")

    def _initialize_rookception(self, session_data):
        thread = threading.Thread(target=self._load_rookception, args=(session_data.model_path,))
        thread.daemon = True
        thread.start()

    def set_cnn(self, cnn):
        self._rookception = cnn

    def update_live_screen(self, img_arr):
        # Update Label with the new screen frame and overlay selection
        height, width, _ = img_arr.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_arr.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Draw overlay
        if self.session_data.selected_region:
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.GlobalColor.red, 2))
            x, y, w, h = self.session_data.selected_region
            painter.drawRect(QRect(x, y, w, h))
            painter.end()

        self.live_screen_label.setPixmap(
            pixmap.scaled(
                self.live_screen_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.store_last_frame(img_arr)

    def update_static_captured_region(self):
        # Display the static captured image of the selected region
        if not self.session_data.temp_chessboard_image:
            print("No captured image found.")
            return

        img_path = self.session_data.temp_chessboard_image
        if not os.path.exists(img_path):
            print(f"Image path does not exist: {img_path}")
            return

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
        height, width, _ = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        self.static_screen_label.setPixmap(
            pixmap.scaled(
                self.static_screen_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def update_overlay(self, region):
        # Force a screen update when the region changes
        if region and self.capture_checkbox.isChecked():
            self.update_live_screen(self.last_frame)

    def store_last_frame(self, img_arr):
        self.last_frame = img_arr

    def update_monitor(self, index):
        self.screen_capture.set_monitor(index + 1)

    def update_fps(self, value):
        self.screen_capture.set_fps(value)

    def toggle_screen_capture(self, live):
        if live:
            self.live_screen_label.setVisible(True)
            self.static_screen_label.setVisible(False)
            self.screen_capture.start_recording()
        else:
            self.live_screen_label.setVisible(False)
            self.static_screen_label.setVisible(True)
            self.screen_capture.stop_recording()

    def _select_chessboard_region(self):
        selector = ScreenRegionSelector(self.screen_capture.get_monitor())
        result = selector.exec()

        if result == QDialog.DialogCode.Accepted:
            selected_area = selector.get_selected_region()
            print("Selected Chessboard Area:", selected_area)

            if selected_area:
                x, y, w, h = selected_area
                img_path = self.screen_capture.capture_static_image(x, y, w, h)
                self.session_data.selected_region = selected_area
                self.session_data.temp_chessboard_image = img_path
                self.update_static_captured_region()

    def _on_get_next_move_clicked(self):
        board_region = self.session_data.selected_region
        board_img_path = self.session_data.temp_chessboard_image
        if not self._rookception or not board_region or not board_img_path:
            return

        self._rookception.predict_board(board_img_path)
