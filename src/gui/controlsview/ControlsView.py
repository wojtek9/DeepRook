from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QCheckBox,
    QFormLayout,
    QSpinBox,
    QButtonGroup,
    QRadioButton,
    QPushButton,
    QScrollArea,
    QToolButton,
    QDoubleSpinBox,
)

from src.bot.ChessBot import ChessBot
from src.session.SessionData import SessionData
from src.utils import uiutils


class ControlsView(QWidget):
    def __init__(self, session_data: SessionData, parent=None):
        super().__init__(parent)

        self.session_data = session_data
        self.bot = ChessBot(session_data=session_data)

        self.session_data.nextMoveChanged.connect(self._make_next_move)

        # Main layout with scroll area
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(
            """
                QScrollArea {
                    border: none;
                }
            """
        )
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.advanced_settings_visible = False

        game_settings_section = QGroupBox("Game Settings")
        game_settings_layout = QVBoxLayout()
        self.color_group = QButtonGroup()
        self.white_button = QRadioButton("Play as White")
        self.black_button = QRadioButton("Play as Black")
        self.white_button.setChecked(True)
        self.color_group.addButton(self.white_button)
        self.color_group.addButton(self.black_button)
        self.color_group.buttonClicked.connect(self.update_game_color)
        game_settings_layout.addWidget(self.white_button)
        game_settings_layout.addWidget(self.black_button)

        game_settings_section.setLayout(game_settings_layout)
        content_layout.addWidget(game_settings_section)

        # Start/Stop Section
        bot_section = QGroupBox("Bot Controls")
        bot_layout = QVBoxLayout()
        # start_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.start_button = QPushButton("Activate")
        self.start_button.clicked.connect(self._on_start_btn_clicked)
        bot_layout.addWidget(self.start_button)

        start_delay_layout = QFormLayout()
        self.start_delay_input = QSpinBox()
        self.start_delay_input.setSuffix(" sec")
        self.start_delay_input.setRange(0, 10)
        start_delay_layout.addRow("Start Delay:", self.start_delay_input)
        bot_layout.addLayout(start_delay_layout)

        movement_layout = QVBoxLayout()
        self.auto_detection_checkbox = QCheckBox("Auto Detection")
        self.auto_detection_checkbox.clicked.connect(self._auto_detection_changed)
        self.auto_move_checkbox = QCheckBox("Auto Move")
        self.auto_move_checkbox.clicked.connect(self._auto_move_changed)
        self.human_movement_checkbox = QCheckBox("Human Mouse Movement")
        self.human_movement_checkbox.clicked.connect(self._human_movement_changed)
        self.random_move_delay_checkbox = QCheckBox("Randomized Move Delay")
        self.random_move_delay_checkbox.clicked.connect(self._on_random_move_time_clicked)

        self.min_move_delay_spbox = QDoubleSpinBox()
        self.min_move_delay_spbox.editingFinished.connect(self._update_move_delay_settings)
        self.min_move_delay_spbox.setRange(0.0, 20.0)
        self.min_move_delay_spbox.setDecimals(1)
        self.min_move_delay_spbox.setSuffix(" sec")
        self.max_move_delay_spbox = QDoubleSpinBox()
        self.max_move_delay_spbox.editingFinished.connect(self._update_move_delay_settings)
        self.max_move_delay_spbox.setRange(0.0, 20.0)
        self.max_move_delay_spbox.setDecimals(1)
        self.max_move_delay_spbox.setSuffix(" sec")

        self.move_delay_layout = QFormLayout()
        self.move_delay_layout.addRow("Min Move Delay:", self.min_move_delay_spbox)
        self.move_delay_layout.addRow("Max Move Delay:", self.max_move_delay_spbox)

        movement_layout.addWidget(self.auto_detection_checkbox)
        movement_layout.addWidget(self.auto_move_checkbox)
        movement_layout.addWidget(self.human_movement_checkbox)
        movement_layout.addWidget(self.random_move_delay_checkbox)
        movement_layout.addLayout(self.move_delay_layout)

        bot_layout.addLayout(movement_layout)
        bot_section.setLayout(bot_layout)
        content_layout.addWidget(bot_section)

        # Movement Section
        # movement_section = QGroupBox("Human-like Behavior")
        # movement_layout = QVBoxLayout()
        # self.human_movement_checkbox = QCheckBox("Human Mouse Movement")
        # self.random_move_delay_checkbox = QCheckBox("Randomized Move Delay")
        # self.random_move_delay_checkbox.clicked.connect(self._on_random_move_time_clicked)
        #
        # self.min_move_delay = QDoubleSpinBox()
        # self.min_move_delay.editingFinished.connect(self._update_move_delay_settings)
        # self.min_move_delay.setRange(0.0, 20.0)
        # self.min_move_delay.setDecimals(1)
        # self.min_move_delay.setSuffix(" sec")
        # self.max_move_delay = QDoubleSpinBox()
        # self.max_move_delay.editingFinished.connect(self._update_move_delay_settings)
        # self.max_move_delay.setRange(0.0, 20.0)
        # self.max_move_delay.setDecimals(1)
        # self.max_move_delay.setSuffix(" sec")
        #
        # self.move_delay_layout = QFormLayout()
        # self.move_delay_layout.addRow("Min Move Delay:", self.min_move_delay)
        # self.move_delay_layout.addRow("Max Move Delay:", self.max_move_delay)
        #
        # movement_layout.addWidget(self.human_movement_checkbox)
        # movement_layout.addWidget(self.random_move_delay_checkbox)
        # movement_layout.addLayout(self.move_delay_layout)
        #
        # movement_section.setLayout(movement_layout)
        # content_layout.addWidget(movement_section)

        # Future Expansion Section
        expansion_section = QGroupBox("Additional Settings")
        expansion_layout = QVBoxLayout()
        self.debug_checkbox = QCheckBox("Enable Debug Logging")
        expansion_layout.addWidget(self.debug_checkbox)
        expansion_section.setLayout(expansion_layout)
        content_layout.addWidget(expansion_section)

        self.advanced_settings_toggle_btn = QToolButton()
        self.advanced_settings_toggle_btn.setText("▲ Advanced Settings")
        self.advanced_settings_toggle_btn.setCheckable(True)
        self.advanced_settings_toggle_btn.setChecked(False)
        self.advanced_settings_toggle_btn.clicked.connect(self._on_advanced_settings_toggle_btn_clicked)
        content_layout.addWidget(self.advanced_settings_toggle_btn)

        # Advanced (Engine) Section with Dropdown
        self.advanced_layout = QVBoxLayout()

        # Engine Selection Section (Initially Hidden)
        self.engine_section = QGroupBox("Engine Settings")
        engine_layout = QVBoxLayout()
        self.engine_group = QButtonGroup()
        self.stockfish_button = QRadioButton("Stockfish")
        self.alphazero_button = QRadioButton("AlphaZero")
        self.leela_button = QRadioButton("Leela")
        self.stockfish_button.setChecked(True)
        self.engine_group.addButton(self.stockfish_button)
        self.engine_group.addButton(self.alphazero_button)
        self.engine_group.addButton(self.leela_button)
        engine_layout.addWidget(self.stockfish_button)
        engine_layout.addWidget(self.alphazero_button)
        engine_layout.addWidget(self.leela_button)

        self.engine_rating_input = QSpinBox()
        self.engine_rating_input.setRange(100, 3500)
        self.engine_rating_input.setSuffix(" Elo")
        engine_layout.addWidget(QLabel("Engine Rating Strength"))
        engine_layout.addWidget(self.engine_rating_input)
        self.engine_section.setLayout(engine_layout)
        self.advanced_layout.addWidget(self.engine_section)

        content_layout.addLayout(self.advanced_layout)

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

        uiutils.toggle_layout_widgets_visible(self.advanced_layout, False)
        self._toggle_move_delay_inputs(False)

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_config()

    def _apply_config(self):
        self.auto_detection_checkbox.setChecked(self.session_data.auto_detection)
        self.auto_move_checkbox.setChecked(self.session_data.auto_move)
        self.human_movement_checkbox.setChecked(self.session_data.human_like_movements)
        self.random_move_delay_checkbox.setChecked(self.session_data.bot_params.random_move_delay)
        self.min_move_delay_spbox.setValue(self.session_data.bot_params.min_move_delay)
        self.max_move_delay_spbox.setValue(self.session_data.bot_params.max_move_delay)

    def _make_next_move(self):
        if self.auto_move_checkbox.isChecked():
            self.bot.move_piece(self.session_data.next_move)

    def update_game_color(self):
        is_white = self.white_button.isChecked()
        self.session_data.play_as_white = is_white

    def _auto_detection_changed(self):
        self.session_data.auto_detection = self.auto_detection_checkbox.isChecked()

    def _auto_move_changed(self):
        self.session_data.auto_move = self.auto_move_checkbox.isChecked()

    def _human_movement_changed(self):
        self.session_data.human_like_movements = self.human_movement_checkbox.isChecked()

    def _on_start_btn_clicked(self):
        # self.bot.play_game()
        pass

    def _on_advanced_settings_toggle_btn_clicked(self):
        self.advanced_settings_visible = not self.advanced_settings_visible
        uiutils.toggle_layout_widgets_visible(self.advanced_layout, self.advanced_settings_visible)
        self.advanced_settings_toggle_btn.setText(
            "▲ Advanced Settings" if not self.advanced_settings_visible else "▼ Advanced Settings"
        )

    def _on_random_move_time_clicked(self):
        is_checked = self.random_move_delay_checkbox.isChecked()
        max_move_delay = self.session_data.bot_params.max_move_delay
        if is_checked:
            self.max_move_delay_spbox.setValue(max_move_delay)
            self._update_move_delay_settings()
        else:
            self.max_move_delay_spbox.setValue(0.0)
        self._toggle_move_delay_inputs(is_checked)
        self.session_data.bot_params.random_move_delay = is_checked

    def _update_move_delay_settings(self):
        min_value = self.min_move_delay_spbox.value()
        max_value = self.max_move_delay_spbox.value()
        if min_value > 0 and min_value > max_value:
            self.max_move_delay_spbox.setValue(min_value)
        self.session_data.bot_params.min_move_delay = min_value
        self.session_data.bot_params.max_move_delay = max_value

    def _toggle_move_delay_inputs(self, enabled):
        self.max_move_delay_spbox.setEnabled(enabled)
        # self.max_move_delay_spbox.setStyleSheet(style)
        # for i in range(self.move_delay_layout.rowCount()):
        #     item = self.move_delay_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
        #     if item:
        #         widget = item.widget()
        #         if widget:
        #             widget.setEnabled(enabled)
        #             widget.setStyleSheet(style)
