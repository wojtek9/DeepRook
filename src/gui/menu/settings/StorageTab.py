from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog


class StorageTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        save_location_label = QLabel("Save Directory:")
        main_layout.addWidget(save_location_label)

        select_dir_button = QPushButton("Select Directory")
        select_dir_button.clicked.connect(self.select_directory)
        main_layout.addWidget(select_dir_button)

    def select_directory(self):
        """Opens a dialog to select a directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            print(f"Selected save directory: {directory}")
