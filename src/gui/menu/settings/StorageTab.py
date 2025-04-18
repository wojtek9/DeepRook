import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QEnterEvent, QDesktopServices
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGridLayout, QStyle, QLineEdit

from src.gui.misc.ClickableLineEdit import ClickableLineEdit
from src.utils import utils


class StorageTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        dirs_grid_layout = QGridLayout()

        cache_location_label = QLabel("Cache Directory")
        cache_location_line_edit = ClickableLineEdit()
        cache_location_line_edit.setText(utils.get_temp_dir())
        cache_location_line_edit.setReadOnly(True)
        cache_location_line_edit.clicked.connect(
            lambda line_edit=cache_location_line_edit: self._on_path_line_edit_clicked(line_edit)
        )
        set_cache_location_btn = QPushButton("...")

        save_location_label = QLabel("Save Directory")
        save_location_line_edit = ClickableLineEdit()
        save_location_line_edit.setReadOnly(True)
        set_save_location_btn = QPushButton("...")

        next_row = 0
        dirs_grid_layout.addWidget(cache_location_label, next_row, 0)
        dirs_grid_layout.addWidget(cache_location_line_edit, next_row, 1)
        dirs_grid_layout.addWidget(set_cache_location_btn, next_row, 2)
        next_row += 1
        dirs_grid_layout.addWidget(save_location_label, next_row, 0)
        dirs_grid_layout.addWidget(save_location_line_edit, next_row, 1)
        dirs_grid_layout.addWidget(set_save_location_btn, next_row, 2)

        main_layout.addLayout(dirs_grid_layout)

    @staticmethod
    def _on_path_line_edit_clicked(line_edit: QLineEdit):
        path = line_edit.text()
        if os.path.exists(path) and os.path.isdir(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def get_open_dir_btn(self):
        btn = QPushButton()
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #31363b;
            }
        """
        )
        btn_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        btn.setIcon(btn_icon)
        return btn

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            print(f"Selected save directory: {directory}")
