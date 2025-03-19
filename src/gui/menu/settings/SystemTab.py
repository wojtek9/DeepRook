from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication


class SystemTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # theme_label = QLabel("Theme:")
        # main_layout.addWidget(theme_label)

        # self.theme_selector = QComboBox()
        # self.theme_selector.addItems(["Light", "Dark"])
        # self.theme_selector.currentIndexChanged.connect(self.change_theme)
        # self.theme_selector.setCurrentIndex(1)
        # main_layout.addWidget(self.theme_selector)

    # def change_theme(self):
    #     selected_theme = self.theme_selector.currentText()
    #     if selected_theme == "Light":
    #         qdarktheme.setup_theme("light")
    #     elif selected_theme == "Dark":
    #         qdarktheme.setup_theme("dark")
