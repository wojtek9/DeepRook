from PySide6.QtCore import Qt
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

        self.settings = {
            "turn": "",
            "start_delay": 0,
            "random_mouse_movement": False,
            "random_move_delay": False,
            "min_move_delay": 0.0,
            "max_move_delay": 5.0,
            "enable_debug_logging": False,
            "engine": "stockfish",
            "engine_rating": 3000,
        }

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

        settings_section = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        self.color_group = QButtonGroup()
        self.white_button = QRadioButton("Play as White")
        self.black_button = QRadioButton("Play as Black")
        self.white_button.setChecked(True)
        self.color_group.addButton(self.white_button)
        self.color_group.addButton(self.black_button)
        settings_layout.addWidget(self.white_button)
        settings_layout.addWidget(self.black_button)

        settings_section.setLayout(settings_layout)
        content_layout.addWidget(settings_section)

        # Start/Stop Section
        bot_section = QGroupBox("Bot Controls")
        bot_layout = QVBoxLayout()
        # start_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.start_button = QPushButton("Start Bot")
        self.start_button.clicked.connect(self._on_start_btn_clicked)
        bot_layout.addWidget(self.start_button)

        start_delay_layout = QFormLayout()
        self.start_delay_input = QSpinBox()
        self.start_delay_input.setSuffix(" sec")
        self.start_delay_input.setRange(0, 10)
        start_delay_layout.addRow("Start Delay:", self.start_delay_input)
        bot_layout.addLayout(start_delay_layout)

        movement_layout = QVBoxLayout()
        self.human_movement_checkbox = QCheckBox("Human Mouse Movement")
        self.random_move_delay_checkbox = QCheckBox("Randomized Move Delay")
        self.random_move_delay_checkbox.clicked.connect(self._on_random_move_time_clicked)

        self.min_move_delay = QDoubleSpinBox()
        self.min_move_delay.editingFinished.connect(self._update_move_delay_settings)
        self.min_move_delay.setRange(0.0, 20.0)
        self.min_move_delay.setDecimals(1)
        self.min_move_delay.setSuffix(" sec")
        self.max_move_delay = QDoubleSpinBox()
        self.max_move_delay.editingFinished.connect(self._update_move_delay_settings)
        self.max_move_delay.setRange(0.0, 20.0)
        self.max_move_delay.setDecimals(1)
        self.max_move_delay.setSuffix(" sec")

        self.move_delay_layout = QFormLayout()
        self.move_delay_layout.addRow("Min Move Delay:", self.min_move_delay)
        self.move_delay_layout.addRow("Max Move Delay:", self.max_move_delay)

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
        max_move_delay = self.settings["max_move_delay"]
        if is_checked:
            self.max_move_delay.setValue(max_move_delay)
            self._update_move_delay_settings()
        else:
            self.max_move_delay.setValue(0.0)
        self._toggle_move_delay_inputs(is_checked)

    def _update_move_delay_settings(self):
        min_value = self.min_move_delay.value()
        max_value = self.max_move_delay.value()
        if min_value > 0 and min_value > max_value:
            self.max_move_delay.setValue(min_value)
        self.settings["min_move_delay"] = min_value
        self.settings["max_move_delay"] = max_value

    def _toggle_move_delay_inputs(self, enabled):
        style = """
                QSpinBox:disabled, QLabel:disabled, QCheckBox:disabled, QLineEdit:disabled {
                    color: gray;
                    background-color: #0d0d0d;
                }
            """
        self.max_move_delay.setEnabled(enabled)
        self.max_move_delay.setStyleSheet(style)
        # for i in range(self.move_delay_layout.rowCount()):
        #     item = self.move_delay_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
        #     if item:
        #         widget = item.widget()
        #         if widget:
        #             widget.setEnabled(enabled)
        #             widget.setStyleSheet(style)
