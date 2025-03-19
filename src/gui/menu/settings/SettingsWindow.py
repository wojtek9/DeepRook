from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QLabel, QPushButton, QApplication

from src.gui.menu.settings.HotkeysTab import HotkeysTab
from src.gui.menu.settings.StorageTab import StorageTab
from src.gui.menu.settings.SystemTab import SystemTab


class SettingsWindow(QDialog):
    def __init__(self, app: QApplication, parent=None):
        super().__init__(parent)

        self.app = app

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.system_settings_tab = SystemTab(app=app)
        self.storage_tab = StorageTab()
        self.hotkeys_tab = HotkeysTab()

        # Add sections
        self.tabs.addTab(self.system_settings_tab, "System")
        self.tabs.addTab(self.storage_tab, "Storage")
        self.tabs.addTab(self.hotkeys_tab, "Hotkeys")

        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)
