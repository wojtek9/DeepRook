import os
import threading
import time

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
    QHBoxLayout,
)
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtCore import Qt, QRect

from src.CNNlayer.Rookception import Rookception
from src.ChessEngine.stockfish.StockfishLayer import StockfishLayer
from src.core.HotkeyListener import HotkeyListener
from src.core.enums.Hotkeys import Hotkey
from src.gui.userscreenview.ScreenCapture import ScreenCapture
from src.gui.userscreenview.ScreenRegionSelector import ScreenRegionSelector
from src.logger.AppLogger import AppLogger
from src.session.SessionData import SessionData
from src.utils import utils


class UserScreenView(QWidget):
    def __init__(self, session_data: SessionData, hotkey_listener: HotkeyListener, parent=None):
        super().__init__(parent)

        self.session_data = session_data
        self.session_data.selectedRegionChanged.connect(self.update_overlay)

        self.hotkey_listener = hotkey_listener
        self.hotkey_listener.hotkeyTriggered.connect(self._hotkey_triggered)

        self._rookception: Rookception | None = None
        self._engine: StockfishLayer | None = None

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
        self.screen_control_layout.addRow("FPS (1-60):", self.fps_selector)

        self.capture_checkbox = QCheckBox("Enable Screen Capture")
        self.capture_checkbox.setChecked(False)
        self.capture_checkbox.toggled.connect(self.toggle_screen_capture)
        self.screen_control_layout.addRow("Live Capture:", self.capture_checkbox)

        # Engine Control Panel
        self.engine_control_panel = QGroupBox("Engine Controls")
        self.engine_control_layout = QVBoxLayout(self.engine_control_panel)
        self.get_best_move_btn = QPushButton("Get Best Move")
        self.get_best_move_btn.clicked.connect(self._on_get_next_move_clicked)
        best_move_layout = QHBoxLayout()
        best_move_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        best_move_title = QLabel("Best Move:")
        best_move_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.best_move_label = QLabel("N/A")
        best_move_layout.addWidget(best_move_title, alignment=Qt.AlignmentFlag.AlignHCenter)
        best_move_layout.addWidget(self.best_move_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.engine_control_layout.addLayout(best_move_layout)
        self.engine_control_layout.addWidget(self.get_best_move_btn)

        self.main_layout.addWidget(self.screen_control_panel)
        self.main_layout.addWidget(self.engine_control_panel)

        screen_capture_layout = QVBoxLayout()
        screen_capture_layout.setContentsMargins(20, 20, 20, 20)
        screen_capture_layout.setSpacing(0)

        # Label for displaying screen capture
        self.live_screen_label = QLabel(self)
        self.live_screen_label.setVisible(False)
        self.live_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.live_screen_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        screen_capture_layout.addWidget(self.live_screen_label)

        # Label for displaying captured region if screen capture is turned off
        self.static_screen_label = QLabel(self)
        self.static_screen_label.setVisible(True)
        self.static_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.static_screen_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        screen_capture_layout.addWidget(self.static_screen_label)

        self.main_layout.addLayout(screen_capture_layout)

    def resizeEvent(self, event):
        # Ensures the static image resizes when the window is resized
        super().resizeEvent(event)

        # Update static screen label to resize the pixmap
        if (
            not self.static_screen_label.pixmap()
            or self.static_screen_label.pixmap().isNull()
            or not self.static_screen_label.isVisible()
        ):
            return

        self.update_static_captured_label()

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_config()
        self._initialize(self.session_data)

    def _apply_config(self):
        pass

    def _hotkey_triggered(self, hotkey: Hotkey):
        match hotkey:
            case Hotkey.MAKE_NEXT_MOVE:
                self.update_next_move()

    def _init_modules(self, model_path):
        self._engine = StockfishLayer()
        AppLogger.debug("Engine loaded")
        self._rookception = Rookception(model_path)
        AppLogger.debug("CNN loaded")

    def _initialize(self, session_data):
        thread = threading.Thread(target=self._init_modules, args=(session_data.model_path,))
        thread.daemon = True
        thread.start()

    def update_live_screen(self, img_arr):
        # Update Label with the new screen frame and overlay selection
        height, width, _ = img_arr.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_arr.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Draw overlay
        if self.session_data.selected_region:
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.GlobalColor.red, 4))
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

    def update_static_captured_label(self):
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

    def update_static_snapshot(self):
        if not self.session_data.selected_region:
            return

        x, y, w, h = self.session_data.selected_region
        board_img_path = self.screen_capture.capture_static_image(x, y, w, h)
        self.session_data.temp_chessboard_image = board_img_path
        return board_img_path

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
                self.update_static_captured_label()

    def _on_get_next_move_clicked(self):
        self.update_next_move()

    def update_next_move(self):
        start_time = time.perf_counter()
        board_region = self.session_data.selected_region
        if not self._rookception or not self._engine or not board_region:
            return

        board_img_path = self.update_static_snapshot()

        board_state = self._rookception.predict_board(board_img_path)
        turn = utils.get_turn_from_play_as_white(self.session_data.play_as_white)
        best_move = self._engine.get_next_move(board_state, turn)
        print("best move: ", best_move)
        if best_move:
            self.session_data.next_move = best_move
            self.best_move_label.setText(best_move)
            # Update again to show new move in label
            self.update_static_snapshot()
            self.update_static_captured_label()
        else:
            self.best_move_label.setText("N/A")

        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"runtime {execution_time:.2f} ms")
